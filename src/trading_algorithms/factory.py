from typing import Callable
from trading_algorithms.indicators import (
    ExponentialMovingAverage,
    Indicator,
    MovingAverageConvergenceDivergence,
    RelativeStrengthIndex,
    SimpleMovingAverage,
)
from trading_algorithms.signals import (
    MovingAverageConvergenceDivergenceSignal,
    MovingAverageCrossoverSignal,
    RelativeStrengthIndexSignal,
    Signal,
)

_indicator_map = {
    "SMA_200": SimpleMovingAverage(),
    "EMA_5": ExponentialMovingAverage(),
    "RSI_14": RelativeStrengthIndex(),
    "MACD": MovingAverageConvergenceDivergence(),
}


def indicator_factory(indicator_name: str) -> Indicator:
    return _indicator_map[indicator_name.upper()]


_signal_map = {
    "MACD": MovingAverageConvergenceDivergenceSignal(),
    "RSI": RelativeStrengthIndexSignal(),
    "MovingAveragCrossover": MovingAverageCrossoverSignal(),
}


def signal_factory(signal_name: str) -> Signal:
    return _signal_map[signal_name.upper()]


IndicatorFactory = Callable[[str], Indicator]
SignalFactory = Callable[[str], Signal]
