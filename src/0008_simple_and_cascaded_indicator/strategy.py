from collections import deque

from nautilus_trader.config import StrategyConfig
from nautilus_trader.indicators.average.ma_factory import (
    MovingAverageFactory,
    MovingAverageType,
)
from nautilus_trader.model.data import Bar, BarType
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

        # 1-min bar type (from config)
        self.bar_type_1min = config.primary_bar_type

        # Indicator: EMA(10) that will be calculated on 1-min bars
        self.indicator_ema10 = MovingAverageFactory.create(10, MovingAverageType.EXPONENTIAL)
        self.indicator_ema10_history = deque()  # we will store historical values here

        # Indicator: Cascaded indicator
        # This will calculate EMA(20) values from of previous EMA(10) indicator calculated on bars
        self.indicator_ema20 = MovingAverageFactory.create(20, MovingAverageType.EXPONENTIAL)
        self.indicator_ema20_history = deque()  # we will store historical values here

    def on_start(self):
        # SUBSCRIBE TO BARS
        # Subscription 1: primary bars (1-min external data)
        self.subscribe_bars(self.config.primary_bar_type)

        # REGISTER INDICATOR to bars, so indicators will automatically feeded by new bars and updated
        # Register indicator
        self.register_indicator_for_bars(self.bar_type_1min, self.indicator_ema10)

        # NOTE:
        # Indicator(s) work that way, that they calculate / store only last value. In case we need
        # to store historical values, we need to store them manually - what we do in this example

    def on_bar(self, bar: Bar):
        self.bars_1min_processed += 1  # Just count 1-min bars

        # Collect historical values of EMA(10)
        # As we registered EMA(10) indicator, we can expect, it automatically has the latest calculated value
        ema_10_current_value = self.indicator_ema10.value
        # Store latest value. We append from left, so value at index 0 is always the latest in list
        self.indicator_ema10_history.appendleft(ema_10_current_value)

        # Calculate cascaded indicator EMA(20) manually
        # Update EMA(20) on indicator EMA(20) on 1-min-bars
        # We need to wait, until EMA(10) is initialized = has first value after first 10 bars
        if self.indicator_ema10.initialized:
            # Feed input value into indicator manually
            self.indicator_ema20.update_raw(self.indicator_ema10.value)
            # Collect historical values
            self.indicator_ema20_history.appendleft(self.indicator_ema20.value)

        # Wait until both indicators are initialized
        # i.e. they have enough input data and have calculated first value)
        if (not self.indicator_ema10.initialized) or (not self.indicator_ema20.initialized):
            self.log.info("Still waiting till both indicators are initialized...")
            return

        # Now we can read indicator values and do whatever we need in our strategy
        # Read latest value directly from indicator
        ema10_last_value = self.indicator_ema10.value
        # Read latest value from history - should provide the same value as previous `ema10_last_value`
        ema10_last_value_from_history = self.indicator_ema10_history[0]
        # Value at 5-bars back is at index 4 (indexing start with 0)
        ema10_value_5_bars_back = self.indicator_ema10_history[4]

        self.log.info(f"EMA(10) latest: {ema10_last_value}, EMA(10) from history: {ema10_last_value_from_history}, EMA(10) 5 bars ago: {ema10_value_5_bars_back}")

    def on_stop(self):
        self.log.info(f"Total 1-min bars processed: {self.bars_1min_processed}")
