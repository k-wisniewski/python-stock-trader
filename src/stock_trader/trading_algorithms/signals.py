from abc import ABC, abstractmethod
from typing import Self

import pandas as pd
from pandas import DataFrame

from src.stock_trader.trading_algorithms.indicators import (
    ExponentialMovingAverage,
    MovingAverageConvergenceDivergence,
    RelativeStrengthIndex,
    SimpleMovingAverage,
)


class Signal(ABC):
    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> str:
        ...


class MovingAverageCrossoverSignal(Signal):
    def __init__(self) -> None:
        self._short_window_days = 5
        self._long_window_days = 200

    def generate_signals(self: Self, data: DataFrame) -> str:
        short_ema_column, long_sma_column = self._calculate_indicators(data)
        return self._calculate_buy_sell_signal_from_indicators(data, short_ema_column, long_sma_column)

    def _calculate_buy_sell_signal_from_indicators(
        self: Self, data: pd.DataFrame, short_ema_column: str, long_sma_column: str
    ) -> str:
        ma_crossover_column = f"Signal_EMA{self._short_window_days}_SMA{self._long_window_days}"
        data.loc[data[short_ema_column] > data[long_sma_column], ma_crossover_column] = 1.0
        data.loc[data[short_ema_column] <= data[long_sma_column], ma_crossover_column] = -1.0
        return ma_crossover_column

    def _calculate_indicators(self: Self, data: pd.DataFrame) -> tuple[str, str]:
        short_ema_column = ExponentialMovingAverage(window_size=self._short_window_days).compute(data)
        long_sma_column = SimpleMovingAverage(window_size=self._long_window_days).compute(data)
        return short_ema_column[0], long_sma_column[0]


class RelativeStrengthIndexSignal(Signal):
    def __init__(self) -> None:
        self._window_size = 14

    def generate_signals(self: Self, data: pd.DataFrame) -> str:
        rsi_signal_column = f"Signal_RSI_{self._window_size}"
        rsi_column = RelativeStrengthIndex(window_size=self._window_size).compute(data)[0]
        data.loc[data[rsi_column] > 70, rsi_signal_column] = -1.0  # Sell signal
        data.loc[data[rsi_column] < 30, rsi_signal_column] = 1.0  # Buy signal
        data.loc[(30 <= data[rsi_column]) & (data[rsi_column] <= 70), rsi_signal_column] = 0.0
        data[rsi_signal_column].fillna(0.0)  # Hold signal
        return rsi_signal_column


class MovingAverageConvergenceDivergenceSignal(Signal):
    def __init__(self) -> None:
        self._short_window_days = 12
        self._long_window_days = 26
        self._signal_window_days = 9

    def generate_signals(self: Self, data: pd.DataFrame) -> str:
        macd_column = f"Signal_MACD_{self._short_window_days}_{self._long_window_days}_{self._signal_window_days}"
        MovingAverageConvergenceDivergence().compute(data)
        data[macd_column] = 0.0
        data.loc[data["MACDLine"] > data["SignalLine"], macd_column] = 1.0  # Buy signal
        data.loc[data["MACDLine"] < data["SignalLine"], macd_column] = -1.0  # Sell signal
        return macd_column
