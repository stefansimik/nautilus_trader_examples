from nautilus_trader.config import StrategyConfig
from nautilus_trader.model import Quantity
from nautilus_trader.model.data import Bar, BarType
from nautilus_trader.model.enums import OrderSide
from nautilus_trader.model.instruments import Instrument
from nautilus_trader.trading.strategy import Strategy
from dataclasses import dataclass

from nautilus_trader.config import StrategyConfig
from nautilus_trader.model.data import Bar, BarType
from nautilus_trader.model.instruments import Instrument
from nautilus_trader.trading.strategy import Strategy
from nautilus_trader.core.message import Event


@dataclass
class Each10thBarEvent(Event):  # Event for each 10th 1-minute bar
    bar: Bar
    TOPIC: str = "each_10th_bar_event"


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

        # Subscribe to event
        self.msgbus.subscribe(Each10thBarEvent.TOPIC, self.on_each_10th_bar)

    def on_bar(self, bar: Bar):
        self.bars_1min_processed += 1  # Just count 1-min bars

        if self.bars_1min_processed % 10 == 0:  # on each 10th bar
            # Publish Event (any strategy can subscribe)
            self.msgbus.publish(Each10thBarEvent.TOPIC, Each10thBarEvent(bar))

    # Event handler
    def on_each_10th_bar(self, event: Each10thBarEvent):
        self.log.info(f"Each10thBarEvent | Bar: {event.bar}")

    def on_stop(self):
        self.log.info(f"Total 1-min bars processed: {self.bars_1min_processed}")
