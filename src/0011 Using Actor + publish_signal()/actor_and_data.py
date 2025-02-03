from nautilus_trader.common.actor import Actor
from nautilus_trader.model.data import BarType

# This actor will generate and publish signal.
# Another Actor/Strategy can subscribe to this signal.
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

        # Publish signal
        self.publish_signal(
            name="signal_count_bars",
            value=self.bars_processed,  # Can send only simple float / int / bool / str value
            ts_event=bar.ts_event,
        )
