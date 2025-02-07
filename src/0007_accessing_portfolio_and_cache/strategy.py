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
        self.bars_1min_processed = 0  # Count processed bars
        self.venue = self.config.instrument.venue

    def on_start(self):
        # Subscribe to bars
        self.subscribe_bars(self.config.primary_bar_type)

    def on_bar(self, bar: Bar):
        self.bars_1min_processed += 1  # Just count 1-min bars

        # Let's simulate at least 1 trade, so strategy has not empty results

        # Buy 1 contract (at specific bar)
        if self.bars_1min_processed == 2:
            # Create order
            order = self.order_factory.market(
                instrument_id=self.config.instrument.id,
                order_side = OrderSide.BUY,
                quantity=Quantity.from_int(1)
            )
            # Submit order
            self.log.info("Submitting entry order.")
            self.submit_order(order)

        # During open position (at 5th bar)
        if self.bars_1min_processed == 5:
            print("Situation is: Open position")
            self.show_data_from_portfolio()
            self.show_data_from_cache()

        # Close previously open position (at specific bar)
        if self.bars_1min_processed == 10:
            self.close_all_positions(instrument_id=self.config.instrument.id)

    def on_stop(self):
        self.log.info(f"Total 1-min bars processed: {self.bars_1min_processed}")

    def show_data_from_portfolio(self):
        # Read values
        portfolio_account = self.portfolio.account(self.venue)
        portfolio_net_exposure = self.portfolio.net_exposure(self.config.instrument.id)
        portfolio_balances_locked = self.portfolio.balances_locked(self.venue)
        portfolio_margins_init = self.portfolio.margins_init(self.venue)
        portfolio_margin_maint = self.portfolio.margins_maint(self.venue)

        # Print values
        self.log.info(f"Portfolio account: {portfolio_account}")
        self.log.info(f"Portfolio net exposure: {portfolio_net_exposure}")
        self.log.info(f"Portfolio balances locked: {portfolio_balances_locked}")
        self.log.info(f"Portfolio margins initial: {portfolio_margins_init}")
        self.log.info(f"Portfolio margin maintenance: {portfolio_margin_maint}")

    def show_data_from_cache(self):
        # Read values
        cache_positions = self.cache.positions()
        cache_orders = self.cache.orders()

        # Print values
        self.log.info(f"Cache positions: {cache_positions}")
        self.log.info(f"Cache orders: {cache_orders}")
