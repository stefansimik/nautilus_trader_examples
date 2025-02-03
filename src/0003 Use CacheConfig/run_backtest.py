import pandas as pd
from nautilus_trader.backtest.engine import BacktestEngine, Decimal
from nautilus_trader.backtest.models import PerContractFeeModel
from nautilus_trader.config import BacktestEngineConfig, CacheConfig, LoggingConfig
from nautilus_trader.model import TraderId
from nautilus_trader.model.currencies import USD
from nautilus_trader.model.data import Bar, BarType
from nautilus_trader.model.enums import AccountType, OmsType
from nautilus_trader.model.identifiers import Venue
from nautilus_trader.model.objects import Money

import utils_csv
import utils_instruments
from strategy import DemoStrategy, DemoStrategyConfig


if __name__ == "__main__":
    # Engine: configure + create
    engine_config = BacktestEngineConfig(
        trader_id=TraderId("BACKTEST_TRADER-001"),
        # FOCUS POINT: configure cache
        cache=CacheConfig(
            bar_capacity=100_000,  # Number of bars stored in Cache (per bar type)
            tick_capacity=100_000,  # Number of ticks stored in Cache (per bar type)
        ),
        logging=LoggingConfig(log_level="DEBUG"),
    )
    engine = BacktestEngine(config=engine_config)

    # Venue: create + add to engine
    #   - Note: Venue must be added first -> before Instrument
    venue: Venue = Venue("GLBX")
    engine.add_venue(
        venue=venue,
        oms_type=OmsType.NETTING,  # Order Management System type
        account_type=AccountType.MARGIN,  # Type of trading account
        starting_balances=[Money(1_000_000, USD)],  # Initial balance
        fee_model=PerContractFeeModel(commission=Money(2.50, USD)),
        base_currency=USD,  # Base currency for the venue
        default_leverage=Decimal(1)
    )

    # Instrument: create + add to engine
    eurusd_future_instrument = (utils_instruments.eurusd_future(2024, 3, venue.value))
    engine.add_instrument(eurusd_future_instrument)

    # BAR DATA: LOAD FROM CSV + ADD TO ENGINE
    # Step 1: Define bar type
    eurusd_future_1min_bar_type = BarType.from_str(f"{eurusd_future_instrument.id}-1-MINUTE-LAST-EXTERNAL")
    # Step 2: Load bar data from CSV file
    eurusd_futures_1min_bars_list: list[Bar] = utils_csv.load_bars_from_ninjatrader_csv(
        csv_path=r"../!market_data/from_ninjatrader/cme/futures/fx/6EH4.GLBX_1min_bars_20240101_20240131.csv",
        instrument=eurusd_future_instrument,
        bar_type=eurusd_future_1min_bar_type,
    )
    # Step 3: Add bars to engine
    engine.add_data(eurusd_futures_1min_bars_list)

    # Strategy: Configure -> create -> add to engine
    strategy_config = DemoStrategyConfig(instrument=eurusd_future_instrument, primary_bar_type=eurusd_future_1min_bar_type)
    strategy = DemoStrategy(strategy_config)
    engine.add_strategy(strategy)

    # Run engine = Run backtest
    engine.run(
        start=None,  # if start is not specified = any first data, that will come will be processed
        end=None,
        streaming=False
    )

    # Optionally print additional strategy results
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

    # Cleanup resources
    engine.dispose()
