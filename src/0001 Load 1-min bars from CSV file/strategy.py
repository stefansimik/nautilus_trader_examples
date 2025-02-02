import time

from nautilus_trader.model.data import Bar, BarType
from nautilus_trader.trading.strategy import Strategy


class DemoStrategy(Strategy):
    def __init__(self, primary_bar_type: BarType):
        super().__init__()
        self.primary_bar_type = primary_bar_type

        self.bar_count = 0
        self.start_time = None

    def on_start(self):
        self.start_time = time.time()
        self.log.info(f"Starting strategy: {self.start_time}")

        # Subscribe to bars
        self.subscribe_bars(self.primary_bar_type)

    def on_bar(self, bar: Bar):
        self.bar_count += 1

        # Print after each 10k bars processed
        if self.bar_count % 10_000 == 0:
            self.log.info(f"Processed {self.bar_count} bars")

    def on_stop(self):
        # Show duration
        end_time = time.time()
        duration = end_time - self.start_time
        self.log.info(f"Total time: {duration:.2f} seconds")

        # Show count bars processed
        self.log.info(f"Total bars processed: {self.bar_count}")

    def on_reset(self):
        self.bar_count = 0
        self.start_time = None
