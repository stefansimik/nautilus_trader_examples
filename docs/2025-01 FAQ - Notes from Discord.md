# FAQ

This document contains frequently asked questions (FAQ) about Nautilus Trader, collected from 
[NautilusTrader - Discord server](https://discord.gg/AUWVs3XaCS).

Note that Nautilus Trader is under active development, and documentation may not always be up to date.

## Data Processing and Aggregation

### Q: How does bar data aggregation work with tick data?
If you add tick data to the BacktestNode or BacktestEngine, the DataEngine can subscribe to this data to build internally aggregated bars. The data source doesn't matter - it can come from either a catalog or elsewhere, as long as it's available to the DataEngine.

### Q: Can higher timeframe bars be created from lower timeframe bars?
Definitely, this is very easy to do and you can find a lot of examples for this - see example: `0006_internally_generated_5min_bars`.

## Order Book and Market Data

### Q: Does Nautilus Trader support order book data?
Yes, Nautilus can handle up to L3 (full depth) order book data. However, for backtesting, you need to provide this data yourself.

### Q: How can I convert Binance data for use with Nautilus Trader?
Examples of data conversion can be found in the repository, specifically in the `examples/backtest/crypto_ema_cross_ethusdt_trailing_stop.py` file.

### Q: Where can I find Level 3 order book data for ES and NQ futures?
Several data vendors provide this data:
- Databento
- Polygon
- DXFeed

## Historical Data and Indicators

### Q: How should I handle historical data requests and live subscriptions?
To avoid interference with indicators:
1. Wait for historical data request completion before subscribing
2. Use the callback to subscribe after indicators are updated
3. Refer to `examples/backtest/databento_test_request_bars.py` for implementation details
4. Use the `request_data` method with appropriate metadatad
5. Use the client parameter to ensure proper query handling

## Backtesting Configuration

### Q: What are the default spread and slippage settings when backtesting with bar data?

Slippage simulation varies based on data type:
- For L2/L3 book data: Fills are simulated per order or price level based on available size
- For top-of-book data (trades, quotes, bars):
  - Default: One tick slippage if top-level size is exhausted
  - Remainder fills at next level
  - Can be disabled with `slip_and_fill_market_orders=False`

## Logging and Debugging

### Q: How can I enable additional logging?
To enable enhanced logging, including Rust network logging:

```python
logging = LoggingConfig(
    log_level="INFO",
    use_pyo3=True,
)
```

Also set the environment variable: `RUST_LOG=debug`

## Network Handling

### Q: How does Nautilus handle network reconnections?
- The trading node continues running unless explicitly stopped (SIGINT/SIGTERM)
- Network disconnections don't shut down the system
- Reconnect functionality has been improved in recent versions
- Note: Version 1.210.0 has a known issue where it may stop after first reconnect failure

## Exchange Integration

### Q: How do I configure leverage for specific instruments on Binance Futures?
Currently, individual instrument leverage adjustment must be done through the exchange GUI.

### Q: Can I monitor websocket latency for order confirmations?
You can measure latency by:
- Comparing OrderAccepted event's `ts_init` with order submission time
- Using the strategy's on_order_accepted handler
- For most purposes, this provides sufficient accuracy (millisecond level)

### Q: Does Nautilus support bracket orders on Binance?
- Sandbox mode: Bracket orders can be simulated
- Live mode: Native bracket order support for Binance is not yet implemented

### Q: Is there a BinanceBarDataWrangler available?
Currently, no specific data wrangler exists for Binance data, but it's being considered for future implementation:
- Could implement a DataFrame-based wrangler
- Alternatively, might add a specific loader similar to Databento or Tardis

### Q: If you get error: TRADER-000.Portfolio: Cannot calculate account state: insufficient data for USDT/USD
This is because you set balance USD rather USDT, just search for USD to locate it and replace.

## Useful libraries and links

### Collections / Curated lists

* **awesome-quant**: https://github.com/wilsonfreitas/awesome-quant (A curated list of insanely awesome libraries, packages and resources for Quants)

### Backtesting

* **Backtesting.py**: https://github.com/kernc/backtesting.py (Backtest trading strategies in Python)
* **QuantStats**: https://github.com/ranaroussi/quantstats (Portfolio analytics for quants, written in Python)

### Charting

* **Plotly**: [Getting started with Plotly in Python](https://plotly.com/python/)
   * [See example](https://html-preview.github.io/?url=https://github.com/stefansimik/dev_demos/blob/main/plotly_trading_charts/Plotly%20-%20Trading%20charts%20examples.html)
* **lightweight-charts-python**: https://github.com/louisnw01/lightweight-charts-python (Python framework for TradingView's Lightweight Charts JavaScript library)
* **mplchart**: https://github.com/furechan/mplchart (Classic Stock Charts in Python)
* **mplfinance**: https://github.com/matplotlib/mplfinance (Financial Markets Data Visualization using Matplotlib)
* **finplot**: https://github.com/highfestiva/finplot (Performant and effortless finance plotting for Python)

### Indicators

* **pandas-ta**: https://github.com/twopirllc/pandas-ta  (Technical Analysis Indicators - Pandas TA is an easy to use Python 3 Pandas Extension with 150+ Indicators)
* **streaming_indicators**: https://github.com/mr-easy/streaming_indicators (A python library for computing technical analysis indicators on streaming data)
* **pytrendseries**: https://github.com/rafa-rod/pytrendseries (Detect trend in time series, drawdown, drawdown within a constant look-back window , maximum drawdown, time underwater)
* **pandas_talib**: https://github.com/femtotrader/pandas_talib (A Python Pandas implementation of technical analysis indicators)
* **finta**: https://github.com/peerchemist/finta (Common financial technical indicators implemented in Pandas)
* **talipp**: https://github.com/nardew/talipp (talipp - incremental technical analysis library for python)
* **market_analy**: https://github.com/maread99/market_analy (Analysis of financial instruments)

### Calendars

* **pandas_market_calendars**: https://github.com/rsheftel/pandas_market_calendars (Exchange calendars to use with pandas for trading applications)
* **exchange_calendars**: https://github.com/gerrymanoim/exchange_calendars (Calendars for various securities exchanges)