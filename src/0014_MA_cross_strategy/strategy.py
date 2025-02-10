from decimal import Decimal

from nautilus_trader.common.enums import LogColor
from nautilus_trader.config import StrategyConfig
from nautilus_trader.core.correctness import PyCondition
from nautilus_trader.indicators.average.ma_factory import MovingAverageFactory
from nautilus_trader.indicators.average.moving_average import MovingAverageType
from nautilus_trader.model.data import Bar, BarType
from nautilus_trader.model.enums import OrderSide, OrderType
from nautilus_trader.model.functions import order_side_to_str
from nautilus_trader.model.instruments import Instrument
from nautilus_trader.model.orders import OrderList
from nautilus_trader.trading.strategy import Strategy


class MACrossStrategyConfig(StrategyConfig, frozen=True):
    instrument: Instrument
    primary_bar_type: BarType
    trade_size: Decimal
    ma_type: MovingAverageType.SIMPLE
    ma_fast_period: int
    ma_slow_period: int
    profit_in_ticks: int
    stoploss_in_ticks: int


class MACrossStrategy(Strategy):
    def __init__(self, config: MACrossStrategyConfig):
        super().__init__(config)

        # Basic checks if configuration makes sense for the strategy
        PyCondition.is_true(
            config.ma_fast_period < config.ma_slow_period,
            "Invalid configuration: Fast MA period {config.ma_fast_period=} must be smaller than slow MA period {config.ma_slow_period=}",
        )

        # Create indicators
        self.ma_fast = MovingAverageFactory.create(
            period=config.ma_fast_period, ma_type=config.ma_type
        )
        self.ma_slow = MovingAverageFactory.create(
            period=config.ma_slow_period, ma_type=config.ma_type
        )

    def on_start(self):
        # Connect indicators with bar-type for automatic updating
        self.register_indicator_for_bars(self.config.primary_bar_type, self.ma_fast)
        self.register_indicator_for_bars(self.config.primary_bar_type, self.ma_slow)

        # Subscribe to bars
        self.subscribe_bars(self.config.primary_bar_type)

    def on_bar(self, bar: Bar):
        self.log.info(f"Bar: {repr(bar)}")

        # Wait until all registered indicators are initialized
        if not self.indicators_initialized():
            count_of_bars = self.cache.bar_count(self.config.primary_bar_type)
            self.log.info(
                f"Waiting for indicators to warm initialize. | Bars count {count_of_bars}",
                color=LogColor.BLUE,
            )
            return

        # Note: If we got here, all registered indicator are initialized

        # BUY LOGIC
        if self.ma_fast.value > self.ma_slow.value:  # If fast EMA is above slow EMA
            if self.portfolio.is_flat(self.config.instrument.id):  # If we are flat
                self.cancel_all_orders(
                    self.config.instrument.id
                )  # Make sure all waiting orders are cancelled
                self.fire_trade(OrderSide.BUY, bar)  # Fire buy order
            if self.portfolio.is_net_short(self.config.instrument.id):  # We are short already
                self.cancel_all_orders(
                    self.config.instrument.id
                )  # Make sure all waiting orders are cancelled
                self.close_all_positions(self.config.instrument.id)  # Let's close current position
                self.fire_trade(OrderSide.BUY, bar)  # Fire buy order

        # SELL LOGIC
        if self.ma_fast.value < self.ma_slow.value:
            if self.portfolio.is_flat(self.config.instrument.id):
                self.cancel_all_orders(self.config.instrument.id)
                self.fire_trade(OrderSide.SELL, bar)
            if self.portfolio.is_net_long(self.config.instrument.id):
                self.cancel_all_orders(self.config.instrument.id)
                self.close_all_positions(self.config.instrument.id)
                self.fire_trade(OrderSide.BUY, bar)

    def fire_trade(self, order_side: OrderSide, last_bar: Bar):
        last_price = last_bar.close

        # Prepare profit/stoploss prices
        if order_side == OrderSide.BUY:
            profit_price = (
                last_price + self.config.profit_in_ticks * self.config.instrument.price_increment
            )
            stoploss_price = (
                last_price - self.config.stoploss_in_ticks * self.config.instrument.price_increment
            )
        elif order_side == OrderSide.SELL:
            profit_price = (
                last_price - self.config.profit_in_ticks * self.config.instrument.price_increment
            )
            stoploss_price = (
                last_price + self.config.stoploss_in_ticks * self.config.instrument.price_increment
            )
        else:
            raise ValueError(f"Order side: {order_side} is not supported.")

        # Prepare bracket order (bracket order is entry order with related contingent profit / stoploss orders)
        bracket_order_list: OrderList = self.order_factory.bracket(
            instrument_id=self.config.instrument.id,
            order_side=order_side,
            quantity=self.config.instrument.make_qty(self.config.trade_size),
            entry_order_type=OrderType.MARKET,  # enter trade with MARKET order
            sl_trigger_price=self.config.instrument.make_price(
                stoploss_price
            ),  # stoploss is always MARKET order (fixed in Nautilus)
            tp_order_type=OrderType.LIMIT,  # profit is LIMIT order
            tp_price=self.config.instrument.make_price(
                profit_price
            ),  # set price for profit LIMIT order
        )

        # Log order
        self.log.info(
            f"Order: {order_side_to_str(order_side)} | Last price: {last_price} | Profit: {profit_price} | Stoploss: {stoploss_price}",
            color=LogColor.BLUE,
        )

        # Submit order
        self.submit_order_list(bracket_order_list)

    def on_stop(self):
        pass
