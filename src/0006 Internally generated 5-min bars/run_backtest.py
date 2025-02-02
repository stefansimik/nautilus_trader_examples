from nautilus_trader.backtest.engine import BacktestEngine
from nautilus_trader.model.data import Bar, BarType, BarSpecification
from nautilus_trader.model.enums import BarAggregation, PriceType
from nautilus_trader.model.identifiers import Venue

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

# Strategy config
config = DemoStrategyConfig(
    instrument=euro_futures_instrument,
    primary_1min_bar_type=euro_futures_bar_type,
    trade_size=1,
)

# Strategy
strategy = DemoStrategy(config)

# Run backtest
engine: BacktestEngine = utils.run_backtest(
    strategy=strategy,
    venue=venue,
    instrument=euro_futures_instrument,
    bars=loaded_bars,
    start=None,
    end=None,
    streaming=True,
    print_backtest_result=True,
    log_level="DEBUG",
)

# Cleanup strategy
engine.reset()
engine.dispose()
