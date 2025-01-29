from nautilus_trader.common.actor import Actor
from nautilus_trader.core.data import Data
from nautilus_trader.model.data import BarType


# Must inherit from Data
class BarCountData(Data):  # Must inherit from Data
    def __init__(self, value: int):
        super().__init__()
        self.value = value


# This actor will generate and publish data with count of bars.
# Another Actor/Strategy can subscribe to this data
class BarCountDataActor(Actor):
    def __init__(self, bar_type: BarType):
        super().__init__()
        self.bar_type = bar_type
        self.bars_processed = 0

    def on_start(self):
        self.subscribe_bars(self.bar_type)
        pass

    def on_bar(self, bar):
        self.bars_processed += 1

        self.publish_signal(
            name="signal_count_bars",
            value=self.bars_processed,  # Can send only simple float / int / bool / str value
            ts_event=bar.ts_event,
        )
