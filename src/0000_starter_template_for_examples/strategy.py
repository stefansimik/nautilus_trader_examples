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
        self.bars_processed = 0

    def on_start(self):
        # Subscribe to bars
        self.subscribe_bars(self.config.primary_bar_type)

    def on_bar(self, bar: Bar):
        self.bars_processed += 1  # Just count 1-min bars

        # Let's simulate at least 1 trade, so strategy has not empty results

        # Buy 1 contract (at specific bar)
        if self.bars_processed == 2:
            # Create order
            order = self.order_factory.market(
                instrument_id=self.config.instrument.id,
                order_side=OrderSide.BUY,
                quantity=Quantity.from_int(1),
            )
            # Submit order
            self.submit_order(order)

        # Close previously open position (at specific bar)
        if self.bars_processed == 5:
            self.close_all_positions(instrument_id=self.config.instrument.id)

    def on_stop(self):
        self.log.info(f"Total 1-min bars processed: {self.bars_processed}")
