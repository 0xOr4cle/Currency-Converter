#!/usr/bin/env python3

import argparse
import json
import os
import sys
import urllib.request
from datetime import datetime

# Constants
API_URL = "https://open.er-api.com/v6/latest/{}"
CACHE_FILE = os.path.expanduser("~/.currency_cache.json")
CACHE_EXPIRY = 24 * 60 * 60  # 24 hours in seconds

def load_cache():
    """Load cached exchange rates"""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def save_cache(cache):
    """Save exchange rates to cache"""
    try:
        with open(CACHE_FILE, 'w') as f:
            json.dump(cache, f, indent=2)
    except:
        pass  # Ignore errors when saving cache

def get_exchange_rates(base_currency):
    """Get exchange rates for a base currency"""
    # Try to get rates from cache first
    cache = load_cache()
    current_time = datetime.now().timestamp()
    
    # Check if we have cached data for this currency that isn't expired
    if base_currency in cache and (current_time - cache[base_currency]["timestamp"] < CACHE_EXPIRY):
        return cache[base_currency]["rates"]
    
    # Otherwise, fetch from API
    try:
        url = API_URL.format(base_currency)
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            
            if data.get("result") == "success":
                # Update cache
                if base_currency not in cache:
                    cache[base_currency] = {}
                
                cache[base_currency]["timestamp"] = current_time
                cache[base_currency]["rates"] = data["rates"]
                save_cache(cache)
                
                return data["rates"]
            else:
                print(f"Error: {data.get('error-type', 'Unknown error')}")
                return None
    except Exception as e:
        print(f"Error fetching exchange rates: {e}")
        
        # If we have any cached data for this currency, use it even if expired
        if base_currency in cache:
            print("Using cached exchange rates (may be outdated)")
            return cache[base_currency]["rates"]
        
        return None

def convert_currency(amount, from_currency, to_currency, rates=None):
    """Convert an amount from one currency to another"""
    if rates is None:
        rates = get_exchange_rates(from_currency)
        if rates is None:
            return None
    
    if to_currency not in rates:
        print(f"Error: Target currency '{to_currency}' not found")
        return None
    
    converted_amount = amount * rates[to_currency]
    return converted_amount

def list_currencies(rates):
    """List all available currencies"""
    print("\nAvailable currencies:")
    # Group currencies in rows of 5
    currencies = sorted(rates.keys())
    for i in range(0, len(currencies), 5):
        row = currencies[i:i+5]
        print("  " + "  ".join(f"{curr}" for curr in row))

def main():
    parser = argparse.ArgumentParser(description="Simple Currency Converter")
    
    parser.add_argument("amount", type=float, nargs="?", help="Amount to convert")
    parser.add_argument("from_currency", nargs="?", help="Source currency code (e.g., USD)")
    parser.add_argument("to_currency", nargs="?", help="Target currency code (e.g., EUR)")
    
    parser.add_argument("-l", "--list", action="store_true", help="List all available currencies")
    parser.add_argument("-a", "--all", action="store_true", help="Show conversion to all currencies")
    parser.add_argument("-c", "--clear-cache", action="store_true", help="Clear cached exchange rates")
    
    args = parser.parse_args()
    
    # Clear cache if requested
    if args.clear_cache:
        if os.path.exists(CACHE_FILE):
            os.remove(CACHE_FILE)
            print("Cache cleared successfully")
        else:
            print("No cache file exists")
        return
    
    # List currencies
    if args.list:
        from_currency = args.from_currency or "USD"
        rates = get_exchange_rates(from_currency)
        if rates:
            print(f"Base currency: {from_currency}")
            list_currencies(rates)
        return
    
    # Convert currency
    if args.amount is None or args.from_currency is None:
        parser.print_help()
        return
    
    # Get exchange rates
    rates = get_exchange_rates(args.from_currency.upper())
    if rates is None:
        return
    
    # Convert to a specific currency
    if args.to_currency and not args.all:
        converted = convert_currency(args.amount, args.from_currency.upper(), args.to_currency.upper(), rates)
        if converted is not None:
            print(f"{args.amount} {args.from_currency.upper()} = {converted:.2f} {args.to_currency.upper()}")
    
    # Convert to all currencies
    elif args.all:
        print(f"\nConversions for {args.amount} {args.from_currency.upper()}:")
        
        # Sort currencies for nicer output
        sorted_rates = sorted(rates.items())
        
        # Find the longest currency code for formatting
        max_len = max(len(curr) for curr in rates.keys())
        
        # Print conversions
        for currency, rate in sorted_rates:
            converted = args.amount * rate
            print(f"  {currency:{max_len}} : {converted:.2f}")
    
    # No target currency specified
    else:
        print("Please specify a target currency or use --all to convert to all currencies")
        list_currencies(rates)

if __name__ == "__main__":
    main()
