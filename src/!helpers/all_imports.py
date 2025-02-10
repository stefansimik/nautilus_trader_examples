# Import Reference Guide
# ---------------------
# This document serves as a comprehensive reference for NautilusTrader imports,
# designed to help developers navigate the correct module paths. All imports are
# organized alphabetically by module path for easy reference. Due to the framework's
# extensive codebase, some classes share names across different modules (e.g., native
# Python implementations versus PyO3 bindings versus Rust classes).
#
# Example: The LogColor class exists in multiple locations:
#
# from nautilus_trader.common.enums import LogColor               # ✓ This is the right one we need to use
# from nautilus_trader.core.nautilus_pyo3 import LogColor         # ✗ Not recommended
# from nautilus_trader.core.nautilus_pyo3.common import LogColor  # ✗ Not recommended
# from nautilus_trader.core.rust.common import LogColor           # ✗ Not recommended

# General pattern is, that you can ignore all imports containing strings:
# * `pyo3`
# * `rust`

from nautilus_trader.analysis.statistic import PortfolioStatistic
from nautilus_trader.analysis.statistics.loser_avg import AvgLoser
from nautilus_trader.analysis.statistics.win_rate import WinRate
from nautilus_trader.analysis.statistics.winner_avg import AvgWinner
from nautilus_trader.backtest.engine import BacktestEngine, BacktestEngineConfig
from nautilus_trader.backtest.models import (
    FeeModel, FillModel, FixedFeeModel, MakerTakerFeeModel, PerContractFeeModel)
from nautilus_trader.cache import Cache, CacheDatabaseAdapter
from nautilus_trader.common import Environment
from nautilus_trader.common.actor import Actor
from nautilus_trader.common.component import (
    LiveClock, TestClock, MessageBus, TimeEventHandler, Subscription, Logger
)
from nautilus_trader.common.config import NautilusConfig
from nautilus_trader.common.enums import ComponentState, ComponentTrigger, LogColor, LogLevel

from  nautilus_trader.common.events import ComponentStateChanged, RiskEvent, TimeEvent, TradingStateChanged

from nautilus_trader.common.executor import ActorExecutor
from nautilus_trader.common.factories import OrderFactory
from nautilus_trader.common.functions import format_utc_timerange
from nautilus_trader.common.providers import InstrumentProvider
from nautilus_trader.config import (
    ActorConfig, ActorFactory, BacktestDataConfig, BacktestEngineConfig, BacktestRunConfig,
    BacktestVenueConfig, CacheConfig, ControllerConfig, ControllerFactory, DataCatalogConfig,
    DataEngineConfig, DatabaseConfig, ExecAlgorithmConfig, ExecAlgorithmFactory, ExecEngineConfig,
    FXRolloverInterestConfig, ImportableActorConfig, ImportableConfig, ImportableControllerConfig,
    ImportableExecAlgorithmConfig, ImportableStrategyConfig, InstrumentProviderConfig,
    InvalidConfiguration, LiveDataClientConfig, LiveDataEngineConfig, LiveExecClientConfig,
    LiveExecEngineConfig, LiveRiskEngineConfig, LoggingConfig, MessageBusConfig,
    NautilusConfig, NautilusKernelConfig, NonNegativeFloat, OrderEmulatorConfig, RiskEngineConfig,
    RoutingConfig, SimulationModuleConfig, StrategyConfig, StrategyFactory, StreamingConfig,
    TradingNodeConfig,
)
from nautilus_trader.core import UUID4, Command, Data, Document, Event, Request, Response
from nautilus_trader.core.correctness import PyCondition
from nautilus_trader.core.data import Data
from nautilus_trader.core.datetime import (
    as_utc_timestamp, dt_to_unix_nanos, format_iso8601, is_datetime_utc, is_tz_aware, micros_to_nanos,
    millis_to_nanos, nanos_to_micros, nanos_to_millis, nanos_to_secs, secs_to_millis, secs_to_nanos,
    unix_nanos_to_dt
)
from nautilus_trader.core.fsm import FiniteStateMachine, InvalidStateTrigger
from nautilus_trader.data.client import DataClient, MarketDataClient
from nautilus_trader.indicators.amat import ArcherMovingAveragesTrends
from nautilus_trader.indicators.aroon import AroonOscillator
from nautilus_trader.indicators.atr import AverageTrueRange
from nautilus_trader.indicators.average.ama import AdaptiveMovingAverage
from nautilus_trader.indicators.average.ema import ExponentialMovingAverage
from nautilus_trader.indicators.average.hma import HullMovingAverage
from nautilus_trader.indicators.average.ma_factory import MovingAverageFactory
from nautilus_trader.indicators.average.moving_average import MovingAverageType, MovingAverage
from nautilus_trader.indicators.average.rma import WilderMovingAverage
from nautilus_trader.indicators.average.sma import SimpleMovingAverage
from nautilus_trader.indicators.average.vidya import VariableIndexDynamicAverage
from nautilus_trader.indicators.average.wma import WeightedMovingAverage
from nautilus_trader.indicators.bias import Bias
from nautilus_trader.indicators.bollinger_bands import BollingerBands
from nautilus_trader.indicators.cci import CommodityChannelIndex
from nautilus_trader.indicators.cmo import ChandeMomentumOscillator
from nautilus_trader.indicators.dm import DirectionalMovement
from nautilus_trader.indicators.donchian_channel import DonchianChannel
from nautilus_trader.indicators.efficiency_ratio import EfficiencyRatio
from nautilus_trader.indicators.fuzzy_candlesticks import FuzzyCandle, FuzzyCandlesticks
from nautilus_trader.indicators.keltner_channel import KeltnerChannel
from nautilus_trader.indicators.keltner_position import KeltnerPosition
from nautilus_trader.indicators.kvo import KlingerVolumeOscillator
from nautilus_trader.indicators.linear_regression import LinearRegression
from nautilus_trader.indicators.macd import MovingAverageConvergenceDivergence
from nautilus_trader.indicators.obv import OnBalanceVolume
from nautilus_trader.indicators.pressure import Pressure
from nautilus_trader.indicators.psl import PsychologicalLine
from nautilus_trader.indicators.roc import RateOfChange
from nautilus_trader.indicators.rsi import RelativeStrengthIndex
from nautilus_trader.indicators.rvi import RelativeVolatilityIndex
from nautilus_trader.indicators.stochastics import Stochastics
from nautilus_trader.indicators.swings import Swings
from nautilus_trader.indicators.vhf import VerticalHorizontalFilter
from nautilus_trader.indicators.volatility_ratio import VolatilityRatio
from nautilus_trader.indicators.vwap import VolumeWeightedAveragePrice
from nautilus_trader.live.config import (
    LiveDataClientConfig, LiveRiskEngineConfig, LiveExecEngineConfig, RoutingConfig,
    LiveExecClientConfig, ControllerConfig, ControllerFactory, TradingNodeConfig)
from nautilus_trader.live.data_client import LiveDataClient, LiveMarketDataClient
from nautilus_trader.live.data_engine import LiveDataEngine
from nautilus_trader.live.execution_client import LiveExecutionClient
from nautilus_trader.live.execution_engine import LiveExecutionEngine
from nautilus_trader.live.factories import LiveDataClientFactory, LiveExecClientFactory
from nautilus_trader.live.node import TradingNode
from nautilus_trader.live.node_builder import TradingNodeBuilder
from nautilus_trader.live.risk_engine import LiveRiskEngine


from nautilus_trader.model.currencies import (
    # Fiat Currencies:
    AUD, BRL, CAD, CHF, CNY, CNH, CZK, DKK, EUR, GBP, HKD, HUF, ILS, INR, JPY, KRW, MXN, NOK, NZD,
    PLN, RUB, SAR, SEK, SGD, THB, TRY, USD, XAG, XAU, ZAR,
    # Crypto Currencies:
    ONEINCH, AAVE, ACA, ADA, AVAX, BCH, BTTC, BNB, BRZ, BSV, BTC, BUSD, XBT, DASH, DOGE, DOT, EOS, ETH,
    ETHW, EZ, FTT, JOE, LINK, LTC, LUNA, NBT, SOL, TRX, TRYB, TUSD, VTC, XLM, XMR, XRP, XTZ, USDC,
    USDC_POS, USDP, USDT, WSB, XEC, ZEC,
)

from nautilus_trader.config import (
    AccountBalance, AccountId, Bar, BarSpecification, BarType, BookLevel, BookOrder, ClientId,
    ClientOrderId, ComponentId, Currency, CustomData, DataType, ExecAlgorithmId, InstrumentClose,
    InstrumentId, InstrumentStatus, MarginBalance, Money, OrderBook, OrderBookDelta,
    OrderBookDeltas, OrderBookDepth10, OrderListId, Position, PositionId, Price, Quantity,
    QuoteTick, StrategyId, Symbol, TradeId, TradeTick, TraderId, Venue, VenueOrderId,
)


from nautilus_trader.model.events import (
    AccountState, OrderAccepted, OrderCancelRejected, OrderCanceled, OrderDenied, OrderEmulated, OrderExpired,
    OrderFilled, OrderInitialized, OrderModifyRejected, OrderPendingCancel, OrderPendingUpdate, OrderRejected,
    OrderReleased, OrderSubmitted, OrderTriggered, OrderUpdated, PositionChanged, PositionClosed, PositionOpened
)

from nautilus_trader.model.instruments import (
    BettingInstrument, BinaryOption,  Cfd, Commodity, CryptoFuture, CryptoPerpetual,
    CurrencyPair, Equity, FuturesContract, FuturesSpread, IndexInstrument, Instrument,
    OptionContract, OptionSpread, SyntheticInstrument
)

from nautilus_trader.model.orders import (
    LimitIfTouchedOrder, LimitOrder, MarketIfTouchedOrder, MarketOrder, MarketToLimitOrder, Order, StopLimitOrder,
    StopMarketOrder, TrailingStopLimitOrder, TrailingStopMarketOrder
)

from nautilus_trader.model.enums import (
    AccountType, AggregationSource, AggressorSide, AssetClass, BarAggregation, BookAction, BookType, ContingencyType,
    CurrencyType, InstrumentClass, InstrumentCloseType, LiquiditySide, MarketStatus, MarketStatusAction, OmsType,
    OptionKind, OrderSide, OrderStatus, OrderType, PositionSide, PriceType, RecordFlag, TimeInForce, TradingState,
    TrailingOffsetType, TriggerType
)

from nautilus_trader.model.functions import (
    account_type_to_str, aggregation_source_to_str, aggressor_side_to_str, asset_class_to_str,
    instrument_class_to_str, bar_aggregation_to_str, book_action_to_str, book_type_to_str,
    contingency_type_to_str, currency_type_to_str, instrument_close_type_to_str, liquidity_side_to_str,
    market_status_to_str, market_status_action_to_str, order_side_to_str, oms_type_to_str,
    option_kind_to_str, order_type_to_str, record_flag_to_str, time_in_force_to_str,
    trading_state_to_str, trailing_offset_type_to_str, trigger_type_to_str,
)

from nautilus_trader.model.identifiers import (
    AccountId, ClientId, ClientOrderId, InstrumentId, OrderListId, PositionId, StrategyId, Symbol, TradeId, TraderId,
    Venue, VenueOrderId
)

from nautilus_trader.model.objects import (
    Quantity, Price, Money, Currency, AccountBalance, MarginBalance
)

from nautilus_trader.model.position import Position

from nautilus_trader.model.venues import (
    CBCM, GLBX, NYUM, XCBT, XCEC, XCME, XFXS, XNYM
)

from nautilus_trader.persistence.catalog import BaseDataCatalog, ParquetDataCatalog

from nautilus_trader.persistence.loaders import (
    CSVTickDataLoader, CSVBarDataLoader, ParquetTickDataLoader, ParquetBarDataLoader,
    InterestRateProviderConfig, InterestRateProvider
)

from nautilus_trader.persistence.wranglers import (
    BarDataWrangler, TradeTickDataWrangler, QuoteTickDataWrangler, OrderBookDeltaDataWrangler
)

from nautilus_trader.persistence.wranglers_v2 import (
    BarDataWranglerV2, TradeTickDataWranglerV2, QuoteTickDataWranglerV2, OrderBookDeltaDataWranglerV2
)

from nautilus_trader.portfolio import Portfolio, PortfolioFacade

from nautilus_trader.risk.engine import RiskEngine
from nautilus_trader.risk.sizing import PositionSizer, FixedRiskSizer

from nautilus_trader.trading import Controller, Strategy, Trader

from nautilus_trader.trading.filters import (
    ForexSession, ForexSessionFilter, NewsImpact, NewsEvent, EconomicNewsEventFilter
)
