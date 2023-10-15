from abc import ABC, abstractmethod
from typing import Self
import pandas as pd


class Indicator(ABC):
    """
    Base class for indicators.
    """

    @abstractmethod
    def compute(self: Self, data: pd.DataFrame) -> list[str]:
        """
        Compute the indicator.

        Args:
        - data (DataFrame): Stock data that will be augmented with the indicator column.

        Returns:
        - Nothing
        """
        ...

    @property
    @abstractmethod
    def columns_for_plot(self: Self) -> list[str]:
        ...


class SimpleMovingAverage(Indicator):
    def __init__(self: Self, window_size: int = 14, column_name: str = "Close") -> None:
        self._window_size = window_size
        self._column_name = column_name

    def compute(self: Self, data: pd.DataFrame) -> list[str]:
        sma_column = f"SMA_{self._window_size}"
        data[sma_column] = data[self._column_name].rolling(window=self._window_size).mean()
        return [sma_column]

    @property
    def columns_for_plot(self: Self) -> list[str]:
        return [f"SMA_{self._window_size}"]


class ExponentialMovingAverage(Indicator):
    def __init__(self: Self, window_size: int = 14, column_name: str = "Close") -> None:
        self._window_size = window_size
        self._column_name = column_name
        self._ema_span = 5

    def compute(self: Self, data: pd.DataFrame) -> list[str]:
        ema_column = f"EMA_{self._window_size}"
        data[ema_column] = data[self._column_name].ewm(span=self._ema_span, adjust=False).mean()
        return [ema_column]

    @property
    def columns_for_plot(self: Self) -> list[str]:
        return [f"EMA_{self._window_size}"]


class RelativeStrengthIndex(Indicator):
    def __init__(self, window_size: int = 14, column_name: str = "Close") -> None:
        self._window_size = window_size
        self._column_name = column_name

    def compute(self: Self, data: pd.DataFrame) -> list[str]:
        delta = data[self._column_name].diff(1)
        gain = delta.clip(lower=0).fillna(0)
        loss = (-delta.clip(upper=0).fillna(0)).replace(-0.0, 0.0)
        avg_gain = pd.Series([0.0] * len(data))
        avg_loss = pd.Series([0.0] * len(data))
        avg_gain[self._window_size] = gain[1 : self._window_size + 1].mean()
        avg_loss[self._window_size] = loss[1 : self._window_size + 1].mean()
        for i in range(self._window_size + 1, len(data)):
            avg_gain.iloc[i] = (avg_gain.iloc[i - 1] * (self._window_size - 1) + gain.iloc[i]) / (self._window_size)
            avg_loss.iloc[i] = (avg_loss.iloc[i - 1] * (self._window_size - 1) + loss.iloc[i]) / (self._window_size)
        rs = avg_gain / avg_loss

        rsi_column = f"RSI_{self._window_size}"
        rs.index = data.index  # make sure rs has the same index as data
        data[rsi_column] = 100 - (100 / (1 + rs))

        return [rsi_column]

    @property
    def columns_for_plot(self: Self) -> list[str]:
        return [f"RSI_{self._window_size}"]


class MovingAverageConvergenceDivergence(Indicator):
    def compute(self, data: pd.DataFrame) -> list[str]:
        macd_line_column, signal_line_column, macd_histogram_column = (
            "MACDLine",
            "SignalLine",
            "MACDHistogram",
        )
        ema_12_column, ema_26_column = "EMA_12", "EMA_26"

        # Compute the 12-day and 26-day EMAs
        data[ema_12_column] = data["Close"].ewm(span=12, adjust=False, min_periods=12).mean()
        data[ema_26_column] = data["Close"].ewm(span=26, adjust=False, min_periods=26).mean()

        # Compute the MACD line
        macd_line = data[ema_12_column] - data[ema_26_column]

        # Compute the signal line
        signal_line = macd_line.ewm(span=9, adjust=False).mean()

        # Compute the MACD histogram
        macd_histogram = macd_line - signal_line

        # Add the MACD-related columns to the DataFrame - TODO: pd.concat

        data[macd_line_column] = macd_line
        data[signal_line_column] = signal_line
        data[macd_histogram_column] = macd_histogram
        return [macd_line_column, signal_line_column, macd_histogram_column]

    @property
    def columns_for_plot(self: Self) -> list[str]:
        return ["MACDLine", "SignalLine", "MACDHistogram", "EMA_12", "EMA_26"]
