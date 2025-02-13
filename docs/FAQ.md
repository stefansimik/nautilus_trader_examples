# FAQ

This document contains frequently asked questions (FAQ) about Nautilus Trader, collected from 
[NautilusTrader - Discord server](https://discord.gg/AUWVs3XaCS).

Note that Nautilus Trader is under active development, and documentation may not always be up to date.

<!-- TOC start (generated with https://github.com/derlin/bitdowntoc) -->

- [Data Processing and Aggregation](#data-processing-and-aggregation)
   * [Q: How does bar data aggregation work with tick data?](#q-how-does-bar-data-aggregation-work-with-tick-data)
   * [Q: Can higher timeframe bars be created from lower timeframe bars?](#q-can-higher-timeframe-bars-be-created-from-lower-timeframe-bars)
- [Order Book and Market Data](#order-book-and-market-data)
   * [Q: Does Nautilus Trader support order book data?](#q-does-nautilus-trader-support-order-book-data)
- [Historical Data and Indicators](#historical-data-and-indicators)
   * [Q: How should I handle historical data requests and live subscriptions?](#q-how-should-i-handle-historical-data-requests-and-live-subscriptions)
- [Backtesting Configuration](#backtesting-configuration)
   * [Q: What are the default spread and slippage settings when backtesting with bar data?](#q-what-are-the-default-spread-and-slippage-settings-when-backtesting-with-bar-data)
- [Development Environment Setup](#development-environment-setup)
   * [Q: How can I fix PyCharm not recognizing NautilusTrader imports?](#q-how-can-i-fix-pycharm-not-recognizing-nautilustrader-imports)
- [Logging and Debugging](#logging-and-debugging)
   * [Q: How can I enable additional logging?](#q-how-can-i-enable-additional-logging)
- [Network Handling](#network-handling)
   * [Q: How does Nautilus handle network reconnections?](#q-how-does-nautilus-handle-network-reconnections)
- [Useful libraries and links](#useful-libraries-and-links)
   * [Collections / Curated lists](#collections-curated-lists)
   * [Backtesting](#backtesting)
   * [Charting](#charting)
   * [Indicators](#indicators)
   * [Calendars](#calendars)

<!-- TOC end -->

<!-- TOC --><a name="data-processing-and-aggregation"></a>
## Data Processing and Aggregation

<!-- TOC --><a name="q-how-does-bar-data-aggregation-work-with-tick-data"></a>
### Q: How does bar data aggregation work with tick data?
If you add tick data to the BacktestNode or BacktestEngine, the DataEngine can subscribe to this data to build internally aggregated bars. The data source doesn't matter - it can come from either a catalog or elsewhere, as long as it's available to the DataEngine.

<!-- TOC --><a name="q-can-higher-timeframe-bars-be-created-from-lower-timeframe-bars"></a>
### Q: Can higher timeframe bars be created from lower timeframe bars?
Definitely, this is very easy to do and you can find a lot of examples for this - see example: `0006_internally_generated_5min_bars`.

<!-- TOC --><a name="order-book-and-market-data"></a>
## Order Book and Market Data

<!-- TOC --><a name="q-does-nautilus-trader-support-order-book-data"></a>
### Q: Does Nautilus Trader support order book data?
Yes, Nautilus can handle up to L3 (full depth) order book data. However, for backtesting, you need to provide this data yourself.

<!-- TOC --><a name="historical-data-and-indicators"></a>
## Historical Data and Indicators

<!-- TOC --><a name="q-how-should-i-handle-historical-data-requests-and-live-subscriptions"></a>
### Q: How should I handle historical data requests and live subscriptions?
To avoid interference with indicators:
1. Wait for historical data request completion before subscribing
2. Use the callback to subscribe after indicators are updated
3. Refer to `examples/backtest/databento_test_request_bars.py` for implementation details
4. Use the `request_data` method with appropriate metadatad
5. Use the client parameter to ensure proper query handling

<!-- TOC --><a name="backtesting-configuration"></a>
## Backtesting Configuration

<!-- TOC --><a name="q-what-are-the-default-spread-and-slippage-settings-when-backtesting-with-bar-data"></a>
### Q: What are the default spread and slippage settings when backtesting with bar data?

Slippage simulation varies based on data type:
- For L2/L3 book data: Fills are simulated per order or price level based on available size
- For top-of-book data (trades, quotes, bars):
  - Default: One tick slippage if top-level size is exhausted
  - Remainder fills at next level
  - Can be disabled with `slip_and_fill_market_orders=False`

<!-- TOC --><a name="development-environment-setup"></a>
## Development Environment Setup

<!-- TOC --><a name="q-how-can-i-fix-pycharm-not-recognizing-nautilustrader-imports"></a>
### Q: How can I fix PyCharm not recognizing NautilusTrader imports?
If you're experiencing issues with PyCharm not recognizing some or all NautilusTrader imports, follow these steps:

1. Ensure you have the latest **PyCharm** version installed (current is 2024.3.2 from Jan 27, 2025)
   * It's recommended to use [JetBrains Toolbox](https://www.jetbrains.com/toolbox-app/) to download directly from JetBrains, as other tools like older versions of Anaconda may not provide the latest version
   * This is especially important if you're using an older version
2. Invalidate all caches in PyCharm: `File -> Invalidate Caches...`
3. Close all PyCharm instances -->  Open your project folder  --> delete the `.idea` folder (this removes all project related settings)
4. Reopen PyCharm with your project and reconfigure your Python interpreter
   * Go to `Settings -> Project: -> Python Interpreter`

<!-- TOC --><a name="logging-and-debugging"></a>
## Logging and Debugging

<!-- TOC --><a name="q-how-can-i-enable-additional-logging"></a>
### Q: How can I enable additional logging?
To enable enhanced logging, including Rust network logging:

```python
engine_config = BacktestEngineConfig(
        trader_id=TraderId("BACKTEST_TRADER-001"),
        logging=LoggingConfig(
          log_level="INFO",        # set level for terminal logging
          log_level_file="DEBUG",  # set level for file logging
          log_directory="logs",    # set your own directory
          use_pyo3=False,          # useful for seeing logs originating from Rust
        ),
    )
)
```

Also set the environment variable: `RUST_LOG=debug`, to enable logs from Rust directly.

<!-- TOC --><a name="network-handling"></a>
## Network Handling

<!-- TOC --><a name="q-how-does-nautilus-handle-network-reconnections"></a>
### Q: How does Nautilus handle network reconnections?
- The trading node continues running unless explicitly stopped (SIGINT/SIGTERM)
- Network disconnections don't shut down the system
- Reconnect functionality has been improved in recent versions
- Note: Version 1.210.0 has a known issue where it may stop after first reconnect failure

<!-- TOC --><a name="useful-libraries-and-links"></a>
## Useful libraries and links

<!-- TOC --><a name="collections-curated-lists"></a>
### Collections / Curated lists

* **awesome-quant**: https://github.com/wilsonfreitas/awesome-quant (A curated list of insanely awesome libraries, packages and resources for Quants)

<!-- TOC --><a name="backtesting"></a>
### Backtesting

* **Backtesting.py**: https://github.com/kernc/backtesting.py (Backtest trading strategies in Python)
* **QuantStats**: https://github.com/ranaroussi/quantstats (Portfolio analytics for quants, written in Python)

<!-- TOC --><a name="charting"></a>
### Charting

* **Plotly**: [Getting started with Plotly in Python](https://plotly.com/python/)
   * [See example](https://html-preview.github.io/?url=https://github.com/stefansimik/dev_demos/blob/main/plotly_trading_charts/Plotly%20-%20Trading%20charts%20examples.html)
* **lightweight-charts-python**: https://github.com/louisnw01/lightweight-charts-python (Python framework for TradingView's Lightweight Charts JavaScript library)
* **mplchart**: https://github.com/furechan/mplchart (Classic Stock Charts in Python)
* **mplfinance**: https://github.com/matplotlib/mplfinance (Financial Markets Data Visualization using Matplotlib)
* **finplot**: https://github.com/highfestiva/finplot (Performant and effortless finance plotting for Python)

<!-- TOC --><a name="indicators"></a>
### Indicators

* **pandas-ta**: https://github.com/twopirllc/pandas-ta  (Technical Analysis Indicators - Pandas TA is an easy to use Python 3 Pandas Extension with 150+ Indicators)
* **streaming_indicators**: https://github.com/mr-easy/streaming_indicators (A python library for computing technical analysis indicators on streaming data)
* **pytrendseries**: https://github.com/rafa-rod/pytrendseries (Detect trend in time series, drawdown, drawdown within a constant look-back window , maximum drawdown, time underwater)
* **pandas_talib**: https://github.com/femtotrader/pandas_talib (A Python Pandas implementation of technical analysis indicators)
* **finta**: https://github.com/peerchemist/finta (Common financial technical indicators implemented in Pandas)
* **talipp**: https://github.com/nardew/talipp (talipp - incremental technical analysis library for python)
* **market_analy**: https://github.com/maread99/market_analy (Analysis of financial instruments)

<!-- TOC --><a name="calendars"></a>
### Calendars

* **pandas_market_calendars**: https://github.com/rsheftel/pandas_market_calendars (Exchange calendars to use with pandas for trading applications)
* **exchange_calendars**: https://github.com/gerrymanoim/exchange_calendars (Calendars for various securities exchanges)