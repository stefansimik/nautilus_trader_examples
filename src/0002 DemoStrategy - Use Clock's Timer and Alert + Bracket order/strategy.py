from datetime import datetime

import pandas as pd
import pytz
from nautilus_trader.common.component import TimeEvent
from nautilus_trader.config import StrategyConfig
from nautilus_trader.model.data import Bar, BarType
from nautilus_trader.model.enums import OrderSide, OrderType, TimeInForce
from nautilus_trader.model.instruments import Instrument
from nautilus_trader.trading.strategy import Strategy


class DemoStrategyConfig(StrategyConfig, frozen=True):
    instrument: Instrument
    primary_bar_type: BarType


class DemoStrategy(Strategy):
    def __init__(self, config: DemoStrategyConfig):
        super().__init__(config)
        self.bar_count = 0
        self.last_price = None

    def on_start(self):
        # Subscribe to bars
        self.subscribe_bars(self.config.primary_1min_bar_type)

        # Recurring timer
        self.clock.set_timer(
            name="every_minute",
            interval=pd.Timedelta(minutes=1),
            callback=self.on_timer,
        )

        # One time - time alert
        self.clock.set_time_alert(
            name="open-trade_alert",
            alert_time=datetime(2024, 11, 4, 11, 0, 0, tzinfo=pytz.utc),
            callback=self.on_alert,
        )

    def on_bar(self, bar: Bar):
        self.bar_count += 1
        self.last_price = bar.close

        if self.bar_count % 100_000 == 0:
            self.log.info(f"Processed {self.bar_count} bars")

    def on_timer(self, event: TimeEvent):
        if event.name == "every_minute":
            self.log.info(f"Event from timer arrived: {event}")

    def on_alert(self, event: TimeEvent):
        if event.name == "open-trade_alert":
            self.log.info(f"Open trade alert detected! - check time: {self.clock.utc_now()}")
            self.fire_bracket_order()

    def fire_bracket_order(self):
        if self.portfolio.is_flat(self.config.instrument.id):
            entry_price = self.last_price
            profit_price = entry_price + (self.config.instrument.price_increment * 20)
            stop_price = entry_price - (self.config.instrument.price_increment * 20)

            bracket_order = self.order_factory.bracket(
                instrument_id=self.config.instrument.id,
                order_side=OrderSide.BUY,
                quantity=self.config.instrument.make_qty(1),
                # Entry
                entry_price=self.config.instrument.make_price(entry_price),
                entry_order_type=OrderType.LIMIT,
                # Profit
                tp_trigger_price=self.config.instrument.make_price(entry_price),
                tp_price=self.config.instrument.make_price(profit_price),
                tp_order_type=OrderType.LIMIT,
                # Stoploss
                sl_trigger_price=self.config.instrument.make_price(stop_price),  # There is only a sl_trigger_price because only StopMarket orders are supported as the SL
                # Other settings
                time_in_force=TimeInForce.GTC,
                tp_post_only=False,
            )

            self.submit_order_list(bracket_order)
            self.log.info(f"Submitted bracket order: entry @ market, TP @ {profit_price}, SL @ {stop_price}")

    def on_stop(self):
        self.log.info(f"Total bars processed: {self.bar_count}")

    def on_reset(self):
        self.bar_count = 0
