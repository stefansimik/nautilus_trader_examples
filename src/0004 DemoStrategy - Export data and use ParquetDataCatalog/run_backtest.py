from nautilus_trader.backtest.engine import BacktestEngine
from nautilus_trader.model.data import Bar, BarType, BarSpecification
from nautilus_trader.model.enums import BarAggregation, PriceType
from nautilus_trader.model.identifiers import Venue
from nautilus_trader.persistence.catalog.parquet import ParquetDataCatalog

import utils
from strategy import DemoStrategyConfig, DemoStrategy

# Prepare Venue
venue: Venue = Venue("SIM")

# Prepare traded instrument
euro_futures_instrument = utils.create_6E_instrument(venue)

# LOAD BARS FROM CSV FILE
# Prepare type
euro_futures_bar_type = BarType(
    instrument_id=euro_futures_instrument.id,
    bar_spec=BarSpecification(step=1, aggregation=BarAggregation.MINUTE, price_type=PriceType.LAST),
)
# Load bar from CSV file
loaded_bars: list[Bar] = utils.load_bars_from_ninjatrader_csv(
    csv_path=r"../!market_data/from_ninjatrader/6E-MAR25__1-Minutes-Bars__Last__from-20241001-to-20241231.csv",
    instrument=euro_futures_instrument,
    bar_type=euro_futures_bar_type,
)

# -------------------------------
# Export to Parquet data catalog
# -------------------------------
data_catalog = ParquetDataCatalog("./temp_data_catalog")
# Write data to catalog
data_catalog.write_data([euro_futures_instrument])  # wrap in list - requires iterable object
data_catalog.write_data(loaded_bars)


# -------------------------------
# Load data Parquet data catalog
# -------------------------------
loaded_bars_from_parquet: list[Bar] = data_catalog.bars(["6E.SIM-1-MINUTE-LAST-EXTERNAL"])


# Strategy config
config = DemoStrategyConfig(
    instrument=euro_futures_instrument,
    primary_bar_type=euro_futures_bar_type,
    trade_size=1,
)

# Strategy
strategy = DemoStrategy(config)

# Run backtest
engine: BacktestEngine = utils.run_backtest(
    strategy=strategy,
    venue=venue,
    instrument=euro_futures_instrument,
    bars=loaded_bars_from_parquet,
    start=None,
    end=None,
    streaming=True,
    print_backtest_result=True,
    log_level="DEBUG",
)

# Cleanup strategy
engine.reset()
engine.dispose()
