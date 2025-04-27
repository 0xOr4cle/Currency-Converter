# 💱 Currency Converter

A simple command-line currency converter using real-time exchange rates.

## ✨ Features

- 💰 Convert between any two currencies
- 🌍 Support for 150+ global currencies
- 📊 Show conversion to all available currencies at once
- 📋 List all supported currencies
- 🔄 Auto-caching of exchange rates to reduce API calls
- 🔌 Works offline using cached rates when internet is unavailable

## 🚀 Installation

1. Clone this repository:
```bash
git clone https://github.com/0xOr4cle/currency-converter.git
cd currency-converter
```

2. Make the script executable (Unix/Linux/macOS):
```bash
chmod +x main.py
```

## 🔍 Usage

```bash
python main.py [amount] [from_currency] [to_currency] [options]
```

## ⚙️ Options

- `amount`: Amount to convert
- `from_currency`: Source currency code (e.g., USD)
- `to_currency`: Target currency code (e.g., EUR)
- `-l, --list`: List all available currencies
- `-a, --all`: Show conversion to all currencies
- `-c, --clear-cache`: Clear cached exchange rates

## 📝 Examples

### Convert a specific amount between two currencies:
```bash
python main.py 100 USD EUR
```

### Convert to all available currencies:
```bash
python main.py 100 USD -a
```

### List all available currencies:
```bash
python main.py -l
```

### List all available currencies with a specific base:
```bash
python main.py -l EUR
```

### Clear the exchange rates cache:
```bash
python main.py -c
```

## 🔄 How It Works

The converter uses the free Exchange Rates API (https://open.er-api.com/) to get the latest exchange rates. To reduce API calls, it caches the rates locally for 24 hours.

When you convert a currency, the tool:
1. Checks if it has cached exchange rates for your base currency
2. Uses the cached rates if available and not expired
3. Otherwise, fetches the latest rates from the API
4. Performs the conversion and displays the result



The cached rates are stored in `~/.currency_cache.json` on your system.