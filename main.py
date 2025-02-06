import argparse
import time
import sys
import platform
import logging
from pathlib import Path
import urllib.request
import subprocess
from colorama import Fore, Style
from api import Binance, Bybit, Coinbase, Bitfinex  # Ensure these are correctly implemented
from arraylib import init_array
from constants import address

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def detect_OS():
    """Check if the OS is Windows"""
    if platform.system() == 'Windows':
        print("This program is running on Windows 7 or later.\n")
        return True
    print("Current OS is not Windows. This program may not work properly.\n")
    return False

def python_version():
    """Check if Python version is 3.x or higher"""
    if sys.version_info >= (3, 0):
        print(f"Python version {sys.version_info[0]}.{sys.version_info[1]} detected. Compatible.\n")
        return True
    print("Python 3 or higher is required.")
    return False

def fetch_price(exchange_func, coin, previous_prices):
    """Fetch and display price from the specified exchange"""
    try:
        price = exchange_func(coin)
        prev_price = previous_prices.get(exchange_func.__name__, 0)
        color = Fore.GREEN if price > prev_price else Fore.RED if price < prev_price else Fore.WHITE
        print(f"{Fore.LIGHTYELLOW_EX}{coin.upper()}{Style.RESET_ALL} price on {exchange_func.__name__} is {color}${price}{Style.RESET_ALL}")
        previous_prices[exchange_func.__name__] = price
    except Exception as e:
        print(f"{Fore.LIGHTYELLOW_EX}{coin.upper()}{Style.RESET_ALL} price on {exchange_func.__name__} is {Fore.RED}not available{Style.RESET_ALL}")
        logging.error(f"Error fetching price from {exchange_func.__name__}: {e}")

def print_divider():
    """Prints a divider for better readability"""
    print(f"{Fore.MAGENTA}{'-' * 50}{Style.RESET_ALL}")

def main():
    if not detect_OS() or not python_version():
        return
    
    parser = argparse.ArgumentParser(
        description="Track cryptocurrency prices from multiple exchanges.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("coin", type=str, help="The cryptocurrency to track.")
    parser.add_argument("--interval", type=int, default=15, help="Time interval in seconds (default: 15).")
    parser.add_argument("--binance", action="store_true", help="Track price from Binance.")
    parser.add_argument("--bybit", action="store_true", help="Track price from Bybit.")
    parser.add_argument("--coinbase", action="store_true", help="Track price from Coinbase.")
    parser.add_argument("--bitfinex", action="store_true", help="Track price from Bitfinex.")
    
    args = parser.parse_args()
    coin = args.coin.lower()
    interval = args.interval

    # Dictionary mapping user arguments to exchange functions
    exchanges = {
        "Binance": Binance,
        "Bybit": Bybit,
        "Coinbase": Coinbase,
        "Bitfinex": Bitfinex
    }

    # Determine which exchanges to track
    selected_exchanges = [name for name, func in exchanges.items() if getattr(args, name.lower())]

    # If no specific exchange is chosen, track all
    if not selected_exchanges:
        print(f"Tracking {Fore.LIGHTYELLOW_EX}{coin.upper()}{Style.RESET_ALL} price on all available exchanges every {Fore.RED}{interval} seconds{Style.RESET_ALL}.\n")
        selected_exchanges = list(exchanges.keys())

    previous_prices = {}

    try:
        while True:
            for exchange_name in selected_exchanges:
                fetch_price(exchanges[exchange_name], coin, previous_prices)
            print_divider()
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == "__main__":
    main()
