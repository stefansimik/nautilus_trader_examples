# FAQ

nautilus_trader is still under active development, the docs is not well updated. Here is the collected questions when I start using it. Most of the contents come from Discord discuss.

##### my data catalog has tick data, but my strategy uses internal bar data. will the aggregation happen when I'mworkingroffuthe catalog?

if you specifically add the tick data to the BacktestNode or BacktestEngine then the DataEngine can subscribe to this data to build the internally aggregated bars. It doesn't matter if the data is coming from the catalog or elsewhere, as long as its available to the DataEngine.

##### Also, if I add 1 minute bar data, will that enable using 5 min bars? ie. do they downsampled the same wayticks are?

Documentation Internal bar aggregation works only with Tick data.

##### Hallo every one, is there any recommendation for drawing tick-level-data plots real-time? using bokeh but it'lagging and slow...tried with hvplot and Holoviz both worse than bokeh...

grafana or other monitoring  
trading view plotlibrary, they look really nice and there is a python wrapper for it  
pygtgraph  
fastht

##### Hi! Is there a way to get order book data from NautilusTrader?

Nautilus can handle up to L3 order book data, but you need to provide it yourself for backtesting.

##### How to convert data from https://data.binance.vision/ to be suitable for Nautilus Trader? Has anyone tried this?

It's a commonly asked question, the information is buried in the repo per the [link](https://github.com/nautechsystems/nautilus_trader/blob/develop/examples/backtest/crypto_ema_cross_ethusdt_trailing_stop.py)

##### Hi all, a question on indicators and historical data 🙂 When I lauch the strategy on_start it requests historical data and subscribes to the feed of that data. However, what if the requested data comes after the first subscription, doesn't that perturb the indicators registered to it as I see that nowhere the order is enforced

It will, if you subscribe only when the data request is completed there can't be any interference  
The callback to subscribe will be called once indicators are updated  
[examples](https://github.com/nautechsystems/nautilus_trader/blob/develop/examples/backtest/databento_test_request_bars.py)
There's a request_data method, you need to populate the metadata appropriately, similarly to what is done for requesting bars or quotes
The metadata of DataType
If you look in actor.pyx you will see what to do, also in engine.pyx, the data engine, in handle_request
usually to avoid interferences there's a client parameter to ensure where your query (request, subscribe, unsubscribe) will be handled.

##### Does anyone know where I can find level 3 orderbook data for es and nq, ideally at least the last 3 months?

databento, polygon, dxfeed ... many vendors out there

##### General backtesting question - what is the default spread/slippage when using bar data for backesting if any?

Slippage is simulated "accurately" if you're using L2 or L3 book data, meaning there will be a fill per order or price level as the available size is matched.
If you're using top-of-book type data (trades, quotes, bars etc.) then we slip one tick if you exhaust the top-level size, then fill the remainder at the next level - by default (unless you set slip_and_fill_market_orders to False yourself, although I think that's less accurate because a market order probably won't behave like an IOC unless you specify that as the time in force)
Acknowledging this needs documenting in the Backtesting concept guide too

##### how to add more log

You could enable additional Rust network logging if you wanted to try running it again:

```python
logging=LoggingConfig(
        log_level="INFO",
        # log_level_file="DEBUG",
        # log_file_format="json",
        use_pyo3=True,  # <---
    ),

```

Also you need the RUST_LOG=debug environment variable. Hope that helps to figure it out, please report when you have a chance to run again and if the issue reoccurs

##### how to engine dealing with reconnect

I see. We were doing the simulation test and manually shut down the network connection. So as long as it successfully starts the trading node, it won't shut down for any connection issues and will be independent from the adapter webosckets. Am I getting right? We are currently trying various edge case tests, since our server might potentially have recurrently network glitches. Do you have any tips for us?

Correct, once the trading node is running - unless explicitly stopped with SIGINT/SIGTERM etc it should keep going. We improved reconnects in the latest version yet to be released.
I think 1.210.0 has an issue that if there's an error on the first reconnect attempt, then it just breaks it's loop and stops (potentially the [problem](https://github.com/nautechsystems/nautilus_trader/blob))

##### Any reason for not using ccxt instead of building from scratch or is there an apetite for using this instead as a crypto adapter?

Short answer is, we've used it in the past. It had many breaking changes, many API features weren't supported so we ended up reaching under the hood to calling the raw exchange APIs anyway, also WebSocket streaming requires a paid for license which was confusing and created friction for users

##### My question is how to configure leverage for specific instrument when running a live trading on binance futures exchange:

Thanks for the kind feedback there. I don't think the platform supports adjusting individual instrument leverage, you might have to do this through the GUI for now?

##### hello, is there any way to monitor websocket latency? for example, monitor how long it takes to get confirmation from binance after a buy/sell order has been sent

You could compare the ts_init of the OrderAccepted event with the time you submit the order from the strategy. There's an on_order_accepted handler for the strategy you could use for this. There's a couple of ways to make this slightly more accurate by adding something into the Binance adapter, but given the internal latency is in the micros, and Binance network latency in the millis, the above should be accurate enough.

##### Does a BinanceBarDataWrangler or similar tooling exist in the library by chance?

Not at this point, but it would certainly be useful. We could either implement a wrangler which takes a dataframe, or a more specific loader along the lines of Databento or Tardis.

##### Hello. Does Nautilus support bracket orders (stop loss, take profit) in Binance sandbox and live modes?

You could simulated Binance with bracket orders in sandbox mode. However, bracket orders haven't been implemented natively for the Binance live adapter yet
