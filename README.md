# coin-price-tracker-script
This code is for tracking cryptocurrency prices from multiple exchanges (Binance, Bybit, Coinbase, Bitfinex) at regular intervals.

# If an exchange’s API is unreachable, the script prints a message
BTC price on Binance is not available

# Tracks BTC price from Binance every 10 seconds.
python main.py btc --binance --interval 10

# Tracks ETH price from Bybit and Coinbase with a default interval of 15 seconds.
python main.py eth --bybit --coinbase
