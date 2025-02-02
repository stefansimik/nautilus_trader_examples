from datetime import datetime, timezone
from decimal import Decimal

import pandas as pd
from nautilus_trader.backtest.engine import BacktestEngine
from nautilus_trader.backtest.models import FillModel
from nautilus_trader.config import BacktestEngineConfig, LoggingConfig
from nautilus_trader.model import TraderId
from nautilus_trader.model.currencies import USD
from nautilus_trader.model.data import Bar, BarType
from nautilus_trader.model.enums import AssetClass, AccountType, OmsType
from nautilus_trader.model.identifiers import Symbol, Venue, InstrumentId
from nautilus_trader.model.instruments import FuturesContract, Instrument
from nautilus_trader.model.objects import Money, Price, Quantity
from nautilus_trader.persistence.wranglers import BarDataWrangler
from nautilus_trader.trading.strategy import Strategy


# noinspection PyPep8Naming,PyArgumentList
def create_6E_instrument(venue: Venue) -> Instrument:
    symbol = Symbol("6E")
    return FuturesContract(
        # Core identification parameters for the Euro FX futures contract
        instrument_id=InstrumentId(symbol, venue),  # 6E is CME's code for EUR/USD futures
        raw_symbol=symbol,  # Symbol as used on the exchange
        asset_class=AssetClass.FX,  # Indicates this is an FX futures contract
        currency=USD,  # Contract is denominated in USD
        # Price and size specifications from CME
        price_precision=5,  # 5 decimal places for EUR/USD pricing
        price_increment=Price(Decimal("0.00005"), precision=5),  # Minimum tick = 0.00005 ($6.25 value)
        multiplier=Quantity(Decimal("125000"), precision=0),  # Each contract = 125,000 EUR
        lot_size=Quantity(Decimal("1"), precision=0),  # Minimum trading size is 1 contract
        # Contract specifications and expiration details
        underlying="EUR/USD",  # The underlying forex pair
        activation_ns=0,  # Contract start time (0 = active now)
        expiration_ns=int(datetime(2099, 12, 17, 14, 16, tzinfo=timezone.utc).timestamp() * 1e9),  # Intentionally too far in the future, so contract is never expired and strategy can run
        # System timestamps for internal tracking
        ts_event=0,  # Event creation time
        ts_init=0,  # Initialization time
        margin_init=Decimal("0.0254"),  # Initial margin $3,500
        margin_maint=Decimal("0.0218"),  # Maintenance margin $3,000
        maker_fee=Decimal("0.0000182"),  # $2.50 per contract maker fee
        taker_fee=Decimal("0.0000182"),  # $2.50 per contract taker fee
        # Additional contract specifications
        exchange="CME",  # Chicago Mercantile Exchange rules
    )


# noinspection PyShadowingNames
def load_bars_from_ninjatrader_csv(csv_path: str, instrument: Instrument, bar_type: BarType) -> list[Bar]:
    # Load data
    # Expects columns ['open', 'high', 'low', 'close', 'volume'] with 'timestamp' index.
    # The 'volume' column is optional, if one does not exist then will use the `default_volume`.
    df = pd.read_csv(csv_path, sep=";", decimal=".", header=0, index_col=False).reindex(columns=["timestamp", "open", "high", "low", "close", "volume"]).assign(timestamp=lambda dft: pd.to_datetime(dft["timestamp"], format="%Y-%m-%d %H:%M:%S")).set_index("timestamp")

    wrangler = BarDataWrangler(bar_type, instrument)
    bars: list[Bar] = wrangler.process(df)
    return bars


def run_backtest(
    strategy: Strategy,
    venue: Venue,
    instrument: Instrument,
    bars: list[Bar],
    start: datetime | str | int | None,
    end: datetime | str | int | None,
    streaming: bool = True,
    print_backtest_result: bool = True,
) -> BacktestEngine:
    # Engine config
    engine_config = BacktestEngineConfig(
        trader_id=TraderId("BACKTEST_TRADER-001"),
        logging=LoggingConfig(
            log_level="DEBUG",       # to stdout
            log_level_file="INFO",   # to file
            log_directory="logs",
            bypass_logging=False,    # set True to bypass logging - for example during optimization (to speedup)
            use_pyo3=False           # enables logs from Rust + set log level by env variable "export RUST_LOG=debug" in command line
        ),
    )

    # Engine
    engine = BacktestEngine(config=engine_config)

    # Add Venue: (note: Venue must be added first -> before Instrument)
    engine.add_venue(
        venue=venue,
        oms_type=OmsType.NETTING,  # Order Management System type
        account_type=AccountType.MARGIN,  # Type of trading account
        starting_balances=[Money(1_000_000, USD)],  # Initial balance
        base_currency=USD,  # Base currency for the venue
        fill_model=FillModel(
            prob_fill_on_limit=0.2,
            prob_fill_on_stop=0.2,
            prob_slippage=0.8,
            random_seed=42
        )
    )

    # Add:
    # - Instrument
    # - Strategy
    # - Bars
    engine.add_instrument(instrument)
    engine.add_strategy(strategy)
    engine.add_data(bars)

    # Run
    engine.run(start=start, end=end, streaming=streaming)

    # Print Results
    if print_backtest_result:
        with pd.option_context(
            "display.max_rows",
            None,  # Show only 10 rows
            "display.max_columns",
            None,  # Show only 10 rows
            "display.width",
            None,
        ):
            n_dashes = 50
            print(f"\n{'-' * n_dashes}\nAccount report for venue: {venue}\n{'-' * n_dashes}")
            print(engine.trader.generate_account_report(venue))

            print(f"\n{'-' * n_dashes}\nOrder fills report: {venue}\n{'-' * n_dashes}")
            print(engine.trader.generate_order_fills_report())

            print(f"\n{'-' * n_dashes}\nPositions report: {venue}\n{'-' * n_dashes}")
            print(engine.trader.generate_positions_report())

    return engine
