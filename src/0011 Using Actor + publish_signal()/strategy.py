# Nautilus trader imports
from nautilus_trader.config import StrategyConfig
from nautilus_trader.model.data import Bar, BarType
from nautilus_trader.model.instruments import Instrument
from nautilus_trader.trading.strategy import Strategy


# Standard library imports


class DemoStrategyConfig(StrategyConfig, frozen=True):
    instrument: Instrument
    primary_1min_bar_type: BarType


class DemoStrategy(Strategy):
    def __init__(self, config: DemoStrategyConfig):
        super().__init__(config)

    def on_start(self):
        # Subscribe to signal
        self.subscribe_signal("signal_count_bars")

    # Handler for all incoming signals
    def on_signal(self, signal):
        self.log.info(f"Signal value: {signal.value}, Signal timestamp: {signal.ts_event}")
        pass

    def on_bar(self, bar: Bar):
        pass

    def on_stop(self):
        pass
