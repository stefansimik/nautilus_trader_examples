from datetime import datetime, timezone

import pandas as pd
from nautilus_trader.backtest.engine import BacktestEngine
from nautilus_trader.backtest.models import MakerTakerFeeModel
from nautilus_trader.config import BacktestEngineConfig, LoggingConfig, StrategyConfig
from nautilus_trader.core.datetime import dt_to_unix_nanos
from nautilus_trader.model.currencies import USD
from nautilus_trader.model.data import Bar, BarSpecification, BarType
from nautilus_trader.model.enums import (
    AccountType,
    BarAggregation,
    OmsType,
    OrderSide,
    PriceType,
    TimeInForce,
)
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

        # Entry market order (at 3rd bar)
        if not self.order_placed and self.bars_processed == 3:
            order = self.order_factory.market(
                instrument_id=self.config.instrument_id,
                order_side=OrderSide.SELL,
                quantity=Quantity.from_int(100_000),
                time_in_force=TimeInForce.GTC,
            )
            self.submit_order(order)
            self.order_placed = True
            self.log.info(f"Market order placed at {bar.close}")

        # Exit market order (at 8th bar)
        if self.order_placed and self.bars_processed == 8:
            order = self.order_factory.market(
                instrument_id=self.config.instrument_id,
                order_side=OrderSide.BUY,
                quantity=Quantity.from_int(100_000),
                time_in_force=TimeInForce.GTC,
            )
            self.submit_order(order)
            self.order_placed = True
            self.log.info(f"Market order placed at {bar.close}")


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
    timestamp_base = dt_to_unix_nanos(datetime(2024, 2, 1, tzinfo=timezone.utc))
    increment = 0.0001
    bars = []
    for i in range(10):
        bar = Bar(
            bar_type=bar_type,
            open=instrument.make_price(1.10000 + i * increment),
            high=instrument.make_price(1.20000 + i * increment),
            low=instrument.make_price(1.10000 + i * increment),
            close=instrument.make_price(1.10000 + i * increment),
            volume=Quantity.from_int(999999),
            ts_event=timestamp_base + (i * 60 * 1_000_000_000),  # +1 minute (in nanoseconds)
            ts_init=timestamp_base + (i * 60 * 1_000_000_000),
        )
        bars.append(bar)

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
