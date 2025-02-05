# Import Reference Guide
# ---------------------
# This document serves as a comprehensive reference for Nautilus Trader imports,
# designed to help developers navigate the correct module paths. All imports are
# organized alphabetically by module path for easy reference. Due to the framework's
# extensive codebase, some classes share names across different modules (e.g., native
# Python implementations versus PyO3 bindings).
#
# Import Resolution Example:
# The ExponentialMovingAverage class exists in multiple locations:
# ✓ from nautilus_trader.indicators.average.ema import ExponentialMovingAverage  # Preferred implementation
# ✗ from nautilus_trader.core.nautilus_pyo3 import ExponentialMovingAverage     # Not recommended

from nautilus_trader.analysis.statistic import PortfolioStatistic
from nautilus_trader.analysis.statistics.loser_avg import AvgLoser
from nautilus_trader.analysis.statistics.winner_avg import AvgWinner
from nautilus_trader.analysis.statistics.win_rate import WinRate
from nautilus_trader.backtest.engine import BacktestEngine, BacktestEngineConfig
from nautilus_trader.backtest.models import (FeeModel, FillModel, FixedFeeModel, MakerTakerFeeModel, PerContractFeeModel)
from nautilus_trader.cache.cache import Cache
from nautilus_trader.common.actor import Actor, ActorConfig, ActorExecutor, ImportableActorConfig
from nautilus_trader.common.component import LiveClock, MessageBus, TestClock, TimeEvent
from nautilus_trader.common.config import NautilusConfig
from nautilus_trader.common.enums import ComponentState, ComponentTrigger, LogColor, LogLevel
from nautilus_trader.common.factories import OrderFactory
from nautilus_trader.common.functions import format_utc_timerange
from nautilus_trader.common.providers import InstrumentProvider
from nautilus_trader.config import (
    ActorConfig, ActorFactory, BacktestDataConfig, BacktestEngineConfig, BacktestRunConfig, BacktestVenueConfig,
    CacheConfig, ControllerConfig, ControllerFactory, DataCatalogConfig, DataEngineConfig, DatabaseConfig,
    ExecAlgorithmConfig, ExecAlgorithmFactory, ExecEngineConfig, FXRolloverInterestConfig, ImportableActorConfig,
    ImportableConfig, ImportableControllerConfig, ImportableExecAlgorithmConfig, ImportableStrategyConfig,
    InstrumentProviderConfig, InvalidConfiguration, LiveDataClientConfig, LiveDataEngineConfig, LiveExecClientConfig,
    LiveExecEngineConfig, LiveRiskEngineConfig, LoggingConfig, MessageBusConfig, NautilusConfig, NautilusKernelConfig,
    NonNegativeFloat, NonNegativeInt, OrderEmulatorConfig, PositiveFloat, PositiveInt, RiskEngineConfig, RoutingConfig,
    SimulationModuleConfig, StrategyConfig, StrategyFactory, StreamingConfig, TradingNodeConfig
)
from nautilus_trader.core.correctness import PyCondition
from nautilus_trader.core.data import Data
from nautilus_trader.core.datetime import (
    as_utc_timestamp, dt_to_unix_nanos, format_iso8601, is_datetime_utc, is_tz_aware, micros_to_nanos,
    millis_to_nanos, nanos_to_micros, nanos_to_millis, nanos_to_secs, secs_to_millis, secs_to_nanos,
    unix_nanos_to_dt
)
from nautilus_trader.core.fsm import FiniteStateMachine, InvalidStateTrigger
from nautilus_trader.core.message import Event
from nautilus_trader.core.uuid import UUID4
from nautilus_trader.data.client import (DataClient, MarketDataClient)
from nautilus_trader.indicators.amat import ArcherMovingAveragesTrends
from nautilus_trader.indicators.aroon import AroonOscillator
from nautilus_trader.indicators.atr import AverageTrueRange
from nautilus_trader.indicators.average.ama import AdaptiveMovingAverage
from nautilus_trader.indicators.average.ema import ExponentialMovingAverage
from nautilus_trader.indicators.average.hma import HullMovingAverage
from nautilus_trader.indicators.average.ma_factory import MovingAverageFactory, MovingAverageType
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
from nautilus_trader.model.currencies import (USD, USDT)
from nautilus_trader.model.data import Bar, BarSpecification, BarType, DataType
from nautilus_trader.model.enums import (
    AccountType, AggregationSource, AggressorSide, AssetClass, BarAggregation, BookAction, BookType, ContingencyType,
    CurrencyType, InstrumentClass, InstrumentCloseType, LiquiditySide, MarketStatus, MarketStatusAction, OmsType,
    OptionKind, OrderSide, OrderStatus, OrderType, PositionSide, PriceType, RecordFlag, TimeInForce, TradingState,
    TrailingOffsetType, TriggerType
)
from nautilus_trader.model.events import (
    AccountState, OrderAccepted, OrderCancelRejected, OrderCanceled, OrderDenied, OrderEmulated, OrderExpired,
    OrderFilled, OrderInitialized, OrderModifyRejected, OrderPendingCancel, OrderPendingUpdate, OrderRejected,
    OrderReleased, OrderSubmitted, OrderTriggered, OrderUpdated, PositionChanged, PositionClosed, PositionOpened
)
from nautilus_trader.model.identifiers import (
    AccountId, ClientId, ClientOrderId, InstrumentId, OrderListId, PositionId, StrategyId, Symbol, TradeId, TraderId,
    Venue, VenueOrderId
)
from nautilus_trader.model.instruments import (FuturesContract, Instrument)
from nautilus_trader.model.objects import AccountBalance, MarginBalance, Money, Price, Quantity
from nautilus_trader.model.orders import (
    LimitIfTouchedOrder, LimitOrder, MarketIfTouchedOrder, MarketOrder, MarketToLimitOrder, Order, StopLimitOrder,
    StopMarketOrder, TrailingStopLimitOrder, TrailingStopMarketOrder
)
from nautilus_trader.model.orders.list import OrderList
from nautilus_trader.model.position import Position
from nautilus_trader.persistence.catalog.parquet import ParquetDataCatalog
from nautilus_trader.persistence.wranglers import (
    BarDataWrangler, OrderBookDeltaDataWrangler, QuoteTickDataWrangler, TradeTickDataWrangler
)
from nautilus_trader.trading.strategy import Strategy