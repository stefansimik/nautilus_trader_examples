from nautilus_trader.config import StrategyConfig
from nautilus_trader.model import Quantity
from nautilus_trader.model.data import Bar, BarType
from nautilus_trader.model.enums import OrderSide
from nautilus_trader.model.instruments import Instrument
from nautilus_trader.trading.strategy import Strategy


class DemoStrategyConfig(StrategyConfig, frozen=True):
    instrument: Instrument
    primary_bar_type: BarType

class DemoStrategy(Strategy):
    def __init__(self, config: DemoStrategyConfig):
        super().__init__(config)
        # Count processed bars
        self.bars_1min_processed = 0

    def on_start(self):
        # Subscribe to bars
        self.subscribe_bars(self.config.primary_bar_type)

        # Subscribe to signal
        self.subscribe_signal("signal_count_bars")

    # Handler for all incoming signals
    def on_signal(self, signal):
        self.log.info(f"Signal value: {signal.value}, Signal timestamp: {signal.ts_event}")

    def on_bar(self, bar: Bar):
        self.bars_1min_processed += 1  # Just count 1-min bars

    def on_stop(self):
        self.log.info(f"Total 1-min bars processed: {self.bars_1min_processed}")
