from nautilus_trader.config import StrategyConfig
from nautilus_trader.model.data import Bar, BarType
from nautilus_trader.model.enums import OrderSide, TimeInForce
from nautilus_trader.model.instruments import Instrument
from nautilus_trader.model.objects import Quantity
from nautilus_trader.trading.strategy import Strategy


class DemoStrategyConfig(StrategyConfig, frozen=True):
    instrument: Instrument
    primary_1min_bar_type: BarType


class DemoStrategy(Strategy):
    def __init__(self, config: DemoStrategyConfig):
        super().__init__(config)
        # Count processed bars
        self.bars_1min_processed = 0
        self.bars_5min_processed = 0
        # New 5-min bar type
        self.bar_type_5min = BarType.from_str(f"{config.instrument.id}-5-MINUTE-LAST-INTERNAL")

    def on_start(self):
        # Subscribe to primary bars (1-min external data)
        self.subscribe_bars(self.config.primary_1min_bar_type)

        # Subscribe to secondary derived bars (5-min internal bars, generated from 1-min external bars)
        self.subscribe_bars(BarType.from_str(f"{self.bar_type_5min}@1-MINUTE-EXTERNAL"))

    def on_bar(self, bar: Bar):
        # Count processed bars (by bar type)
        match bar.bar_type:
            case self.config.primary_1min_bar_type:
                self.bars_1min_processed += 1
            case self.bar_type_5min:
                self.bars_5min_processed += 1
            case _:
                raise Exception(f"Bar type {bar.bar_type} not handled in on_bar")

        # Enter position: on 5th (5-min bar)
        if self.bars_5min_processed == 5:
            order = self.order_factory.market(
                instrument_id=self.config.instrument.id,
                order_side=OrderSide.BUY,
                quantity=Quantity.from_str("1"),
                time_in_force=TimeInForce.GTC,
            )
            self.submit_order(order)
            self.log.info("Entering position.")

        # Close position: on 8th (5-min bar)
        if self.bars_5min_processed == 8:
            self.close_all_positions(instrument_id=self.config.instrument.id)
            self.log.info("Closing position.")

    def on_stop(self):
        self.log.info(f"Total 1-min bars processed: {self.bars_1min_processed}")
        self.log.info(f"Total 5-min bars processed: {self.bars_5min_processed}")

    def on_reset(self):
        self.bars_1min_processed = 0
        self.bars_5min_processed = 0
