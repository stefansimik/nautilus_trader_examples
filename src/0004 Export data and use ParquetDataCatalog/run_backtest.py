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
euro_futures_bar_type = BarType.from_str(f"{euro_futures_instrument.id}-1-MINUTE-LAST-EXTERNAL")

# Load bar from CSV file
loaded_bars: list[Bar] = utils.load_bars_from_ninjatrader_csv(
    csv_path=r"../!market_data/from_ninjatrader/6E-MAR25__1-Minutes-Bars__Last__from-20241001-to-20241231.csv",
    instrument=euro_futures_instrument,
    bar_type=euro_futures_bar_type,
)

# -------------------------------------------
# Create catalog
# -------------------------------------------

# Create data catalog
data_catalog = ParquetDataCatalog("./temp_data_catalog")

# -------------------------------------------
# Add data to catalog
# -------------------------------------------

# Add new instrument to catalog
data_catalog.write_data([euro_futures_instrument])  # wrap in list - requires iterable object

# Add new bars to catalog
data_catalog.write_data(loaded_bars)

# -------------------------------------------
# Read data from catalog
# -------------------------------------------

# Read all instruments
all_instruments = data_catalog.instruments()

# Returns bars for all available bar_types
all_bars = data_catalog.bars()

# Returns bars - but filter only specific bar_types
euro_futures_bars_from_parquet = data_catalog.bars(["6E.SIM-1-MINUTE-LAST-EXTERNAL"])

# Strategy config
config = DemoStrategyConfig(
    instrument=euro_futures_instrument,
    primary_bar_type=euro_futures_bar_type,
)

# Strategy
strategy = DemoStrategy(config)

# Run backtest
engine: BacktestEngine = utils.run_backtest(
    strategy=strategy,
    venue=venue,
    instrument=euro_futures_instrument,
    bars=euro_futures_bars_from_parquet,
    start=None,
    end=None,
    streaming=True,
    print_backtest_result=True,
    log_level="DEBUG",
)

# Cleanup strategy
engine.reset()
engine.dispose()
