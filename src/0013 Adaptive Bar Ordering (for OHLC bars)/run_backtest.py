from datetime import datetime, timezone
from decimal import Decimal

import pandas as pd
from nautilus_trader.backtest.engine import BacktestEngine
from nautilus_trader.backtest.models import PerContractFeeModel
from nautilus_trader.config import BacktestEngineConfig, LoggingConfig, StrategyConfig
from nautilus_trader.core.datetime import dt_to_unix_nanos
from nautilus_trader.model.currencies import USD
from nautilus_trader.model.data import Bar, BarType, BarSpecification
from nautilus_trader.model.enums import (
    AccountType,
    AssetClass,
    BarAggregation,
    OmsType,
    PriceType,
)
from nautilus_trader.model.identifiers import InstrumentId, Symbol, TraderId, Venue
from nautilus_trader.model.instruments import FuturesContract
from nautilus_trader.model.objects import Money, Price, Quantity
from nautilus_trader.trading.strategy import Strategy


def create_6E_instrument(venue: Venue) -> FuturesContract:
    symbol = Symbol("6E")
    return FuturesContract(
        # Core identification parameters for the Euro FX futures contract
        instrument_id=InstrumentId(symbol, venue),  # 6E is CME's code for EUR/USD futures
        raw_symbol=symbol,  # Symbol as used on the exchange
        asset_class=AssetClass.FX,  # Indicates this is an FX futures contract
        currency=USD,  # Contract is denominated in USD
        # Price and size specifications from CME
        price_precision=5,  # 5 decimal places for EUR/USD pricing
        price_increment=Price(Decimal("0.00005"), precision=5),  # Minimum tick = 0.00005 ($6.25 value)
        multiplier=Quantity(Decimal("125000"), precision=0),  # Each contract = 125,000 EUR
        lot_size=Quantity(Decimal("1"), precision=0),  # Minimum trading size is 1 contract
        # Contract specifications and expiration details
        underlying="EUR/USD",  # The underlying forex pair
        activation_ns=0,  # Contract start time (0 = active now)
        expiration_ns=int(datetime(2099, 12, 17, 14, 16, tzinfo=timezone.utc).timestamp() * 1e9),  # 3rd Wednesday at 9:16 AM CT
        # System timestamps for internal tracking
        ts_event=0,  # Event creation time
        ts_init=0,  # Initialization time
        margin_init=Decimal("0.21818181812"),  # $3_000 per contract (at price 1.1000). This amount must be available to open new position. It is not block, it is only entry requirement check.
        margin_maint=Decimal("0.18181818182"),  # $2,500 per contract (at price 1.1000). This amount is really locked on account, while we have open position
        maker_fee=Decimal("0"),  # CME Futures don't use maker/taker fee model. They have fixed fee per contract.
        taker_fee=Decimal("0"),  # same as above
        # Additional contract specifications
        exchange="SIM",  # Chicago Mercantile Exchange rules
    )


class MinimalStrategyConfig(StrategyConfig, frozen=True):
    instrument_id: InstrumentId
    bar_type: BarType


class MinimalStrategy(Strategy):
    def __init__(self, config: MinimalStrategyConfig):
        super().__init__(config)
        self.bars_processed = 0

    def on_start(self):
        self.subscribe_bars(self.config.bar_type)

    def on_bar(self, bar: Bar):
        self.bars_processed += 1

    def on_stop(self):
        self.log.info(f"Count of processed bars: {self.bars_processed}")


if __name__ == "__main__":
    # Engine config
    engine_config = BacktestEngineConfig(
        trader_id=TraderId("BACKTEST_TRADER-001"),
        logging=LoggingConfig(log_level="debug"),
    )

    # Engine
    engine = BacktestEngine(config=engine_config)

    # Venue
    venue = Venue("SIM")
    engine.add_venue(
        venue=venue,
        oms_type=OmsType.NETTING,
        account_type=AccountType.MARGIN,
        base_currency=USD,
        fee_model=PerContractFeeModel(Money(2.50, USD)),
        starting_balances=[Money(1_000_000, USD)],
        bar_adaptive_high_low_ordering=True,  # <-------------- THIS IS THE IMPORTANT SETTINGS
        # Note:
        # If bar_adaptive_high_low_ordering=True,
        #   then Nautilus uses intelligent statistical heuristics to model, if High / Low of the bar should be modeled as first.
        # If bar_adaptive_high_low_ordering=False,
        #   then Nautilus uses fixed static OHLC order (High is first always)
    )

    # Instrument
    instrument = create_6E_instrument(venue)
    engine.add_instrument(instrument)

    # Add data = just 3 bars with same OHLC prices
    bar_type = BarType(
        instrument_id=instrument.id,
        bar_spec=BarSpecification(step=1, aggregation=BarAggregation.MINUTE, price_type=PriceType.LAST),
    )

    # Generate artificial 1-min bars
    timestamp_base = dt_to_unix_nanos(datetime(2024, 1, 1, tzinfo=timezone.utc))
    increment = 0.0001
    bars = []

    # Bar 1: Expected order is OHLC (High first) - see Debug logs
    bar1 = Bar(
        bar_type=bar_type,
        open=instrument.make_price(1.30000),
        high=instrument.make_price(1.40000),
        low=instrument.make_price(1.10000),
        close=instrument.make_price(1.20000),
        volume=Quantity.from_str("100"),
        ts_event=timestamp_base + (1 * 60_000_000_000),  # +1 minute
        ts_init=timestamp_base + (1 * 60_000_000_000),
    )
    bars.append(bar1)

    # Bar 1: Expected order is OLHC (Low first) - see Debug logs
    bar2 = Bar(
        bar_type=bar_type,
        open=instrument.make_price(1.20000),
        high=instrument.make_price(1.40000),
        low=instrument.make_price(1.10000),
        close=instrument.make_price(1.30000),
        volume=Quantity.from_str("100"),
        ts_event=timestamp_base + (2 * 60_000_000_000),  # +1 minute
        ts_init=timestamp_base + (2 * 60_000_000_000),
    )
    bars.append(bar2)

    # Add all created bars
    engine.add_data(bars)

    # Create strategy
    config = MinimalStrategyConfig(
        instrument_id=instrument.id,
        bar_type=bar_type,
    )
    strategy = MinimalStrategy(config=config)
    engine.add_strategy(strategy)

    # Run backtest
    engine.run()

    # Print reports
    with pd.option_context(
        "display.max_rows",
        None,  # Show only 10 rows
        "display.max_columns",
        None,  # Show only 10 rows
        "display.width",
        None,
    ):
        n_dashes = 50
        print(f"\n{'-' * n_dashes}\nAccount report for venue: {venue}\n{'-' * n_dashes}")
        print(engine.trader.generate_account_report(venue))

        print(f"\n{'-' * n_dashes}\nOrder fills report: {venue}\n{'-' * n_dashes}")
        print(engine.trader.generate_order_fills_report())

        print(f"\n{'-' * n_dashes}\nPositions report: {venue}\n{'-' * n_dashes}")
        print(engine.trader.generate_positions_report())

    # Cleanup
    engine.dispose()
