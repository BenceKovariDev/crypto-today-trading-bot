# Algorithmic Crypto Trading Bot with Live Monitor

An automated Python trading script using the Bybit/Binance API to track real-time market movements, filter top volume assets, and execute a momentum strategy with strict risk management.

## Features
- **Top 50 Volume Filter:** Dynamically tracks the top 50 highest-turnover crypto assets in USD to ensure high liquidity.
- **Momentum Entry:** Automatically identifies assets with strong daily positive percentage gains.
- **Risk Management:** Enforces a hard **-1.00% Stop-Loss** on all active positions to minimize downside risk.
- **Live Terminal Dashboard:** Features a clean, self-refreshing live terminal interface showing open positions, profit/loss tracking, market leaders, and transaction logs.

## Tech Stack
- **Language:** Python 3
- **Libraries:** `requests`, `time`, `os`
- **API Integration:** Bybit V5 Market API# crypto-today-trading-bot
