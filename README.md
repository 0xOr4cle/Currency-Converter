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
git clone https://github.com/yourusername/currency-converter.git
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

