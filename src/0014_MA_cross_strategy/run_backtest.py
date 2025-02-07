import pandas as pd
from nautilus_trader.backtest.engine import BacktestEngine, Decimal
from nautilus_trader.backtest.models import (FillModel, PerContractFeeModel)
from nautilus_trader.config import BacktestEngineConfig, LoggingConfig
from nautilus_trader.indicators.average.moving_average import MovingAverageType
from nautilus_trader.model import TraderId
from nautilus_trader.model.currencies import USD
from nautilus_trader.model.data import Bar, BarType
from nautilus_trader.model.enums import AccountType, OmsType
from nautilus_trader.model.identifiers import Venue
from nautilus_trader.model.objects import Money

import utils_csv
import utils_instruments
from strategy import MACrossStrategy, MACrossStrategyConfig


if __name__ == "__main__":
    # Engine: configure + create
    engine_config = BacktestEngineConfig(
        trader_id=TraderId("BACKTEST_TRADER-001"),
        logging=LoggingConfig(log_level="INFO", log_level_file='DEBUG', log_directory='logs'),
    )
    engine = BacktestEngine(config=engine_config)

    # Venue: create + add to engine
    # Note: Venue must be added first -> before Instrument
    venue: Venue = Venue("GLBX")
    engine.add_venue(
        venue=venue,
        oms_type=OmsType.NETTING,  # Order Management System type
        account_type=AccountType.MARGIN,  # Type of trading account
        starting_balances=[Money(1_000_000, USD)],  # Initial balance
        fee_model=PerContractFeeModel(commission=Money(2.36, USD)),
        base_currency=USD,  # Base currency for the venue
        default_leverage=Decimal(1),
        fill_model=FillModel(
            prob_fill_on_limit=0,  # 0 = 0% probability = never fill market touches limit price
            prob_fill_on_stop=0,   # 0 = 0% probability =  never fill at stop-price when market touches stop-price
            prob_slippage=1,       # 1 = 100% probability =  always simulate 1-tick slippage with market order
            random_seed=42,        # fixed random seed for reproducible results
        )
    )

    # Instrument: create + add to engine
    eurusd_future_instrument = (utils_instruments.eurusd_future(2024, 3, venue.value))
    engine.add_instrument(eurusd_future_instrument)

    # BAR DATA: LOAD FROM CSV + ADD TO ENGINE
    # Step 1: Define bar type
    eurusd_future_1min_bar_type = BarType.from_str(f"{eurusd_future_instrument.id}-1-MINUTE-LAST-EXTERNAL")
    # Step 2: Load bar data from CSV file
    eurusd_futures_1min_bars_list: list[Bar] = utils_csv.load_bars_from_ninjatrader_csv(
        csv_path=r"../!market_data/cme/futures/fx/6EH4.GLBX_1min_bars_20240101_20240131.csv",
        instrument=eurusd_future_instrument,
        bar_type=eurusd_future_1min_bar_type,
    )
    # Step 3: Add bars to engine
    engine.add_data(eurusd_futures_1min_bars_list)

    # Strategy: Configure -> create -> add to engine
    strategy_config = MACrossStrategyConfig(
        instrument=eurusd_future_instrument,
        primary_bar_type=eurusd_future_1min_bar_type,
        trade_size=Decimal(1),
        ma_type=MovingAverageType.SIMPLE,
        ma_fast_period=20,
        ma_slow_period=50,
        profit_in_ticks=20,
        stoploss_in_ticks=20,
    )
    strategy = MACrossStrategy(strategy_config)
    engine.add_strategy(strategy)

    # Run engine = Run backtest
    engine.run(
        start=None, #'2024-01-25',  # if start is not specified = any first data, that will come will be processed
        end='2024-01-03',
        streaming=False
    )

    # Optionally print additional strategy results
    print_additional_results = False  # this strategy produces huge outputs, so we disable it
    if print_additional_results:
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
