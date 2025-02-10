from datetime import datetime, timezone

import pandas as pd
from nautilus_trader.backtest.engine import BacktestEngine
from nautilus_trader.backtest.models import MakerTakerFeeModel
from nautilus_trader.config import BacktestEngineConfig, LoggingConfig, StrategyConfig
from nautilus_trader.core.datetime import dt_to_unix_nanos
from nautilus_trader.model.currencies import USD
from nautilus_trader.model.data import Bar, BarSpecification, BarType
from nautilus_trader.model.enums import AccountType, BarAggregation, OmsType, PriceType
from nautilus_trader.model.identifiers import InstrumentId, TraderId, Venue
from nautilus_trader.model.objects import Money, Quantity
from nautilus_trader.test_kit.providers import TestInstrumentProvider
from nautilus_trader.trading.strategy import Strategy


class MinimalStrategyConfig(StrategyConfig, frozen=True):
    instrument_id: InstrumentId
    bar_type: BarType


class MinimalStrategy(Strategy):
    def __init__(self, config: MinimalStrategyConfig):
        super().__init__(config)
        self.order_placed = False
        self.bars_processed = 0

    def on_start(self):
        self.subscribe_bars(self.config.bar_type)

    def on_bar(self, bar: Bar):
        self.bars_processed += 1

    def on_stop(self):
        self.log.info(f"Strategy stopped. | Count of bars processed: {self.bars_processed}")


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
        fee_model=MakerTakerFeeModel(),
        starting_balances=[Money(1_000_000, USD)],
        # FOCUS POINT:
        # If bar_adaptive_high_low_ordering=True,
        #   then Nautilus uses intelligent statistical heuristics to model, if High / Low of the bar should be modeled as first.
        # If bar_adaptive_high_low_ordering=False,
        #   then Nautilus uses fixed static OHLC order (High is first always)
        bar_adaptive_high_low_ordering=True,
        # Run strategy and see the debug logs, how bar_adaptive_high_low_ordering=True
        # ensures, that first High / Low is simulated based on statistical probability.
    )

    # Instrument
    instrument = TestInstrumentProvider.default_fx_ccy("EUR/USD", venue)
    engine.add_instrument(instrument)

    # Add data = just 3 bars with same OHLC prices
    bar_type = BarType(
        instrument_id=instrument.id,
        bar_spec=BarSpecification(
            step=1, aggregation=BarAggregation.MINUTE, price_type=PriceType.LAST
        ),
    )

    # Generate artificial 1-min bars
    timestamp_base = dt_to_unix_nanos(datetime(2024, 1, 1, tzinfo=timezone.utc))
    increment = 0.0001
    bars = []

    # Bar 1: Expected order is OHLC (High first) - see debug logs
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

    # Bar 1: Expected order is OLHC (Low first) - see debug logs
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
