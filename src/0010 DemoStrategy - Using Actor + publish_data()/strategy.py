# Nautilus trader imports
from nautilus_trader.config import StrategyConfig
from nautilus_trader.core.data import Data
from nautilus_trader.model.data import Bar, BarType, DataType
from nautilus_trader.model.instruments import Instrument
from nautilus_trader.trading.strategy import Strategy

from actor_and_data import BarCountData


# Standard library imports


class DemoStrategyConfig(StrategyConfig, frozen=True):
    instrument: Instrument
    primary_1min_bar_type: BarType


class DemoStrategy(Strategy):
    def __init__(self, config: DemoStrategyConfig):
        super().__init__(config)

    def on_start(self):
        # Subscribe to data -> will be handled in `on_data` callback
        self.subscribe_data(DataType(BarCountData))

    # Handler for all incoming Data objects
    def on_data(self, data: Data):
        if isinstance(data, BarCountData):
            print(f"BarsProcessedData received. | Value: {data.value}")

    def on_bar(self, bar: Bar):
        pass

    def on_stop(self):
        pass
