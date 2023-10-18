from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Self
import matplotlib.pyplot as plt
import mplfinance as mpf
import numpy as np
import pandas as pd

from stock_trader.settings import APP_SETTINGS

Subplot = dict[str, pd.Series | pd.DataFrame | np.ndarray | list]


class Visualizer(ABC):
    def __init__(self: Self, next_visualizer: Optional["Visualizer"] = None) -> None:
        self._next_visualizer = next_visualizer

    @abstractmethod
    def _can_draw_indicator(self: Self, indicator_name: str) -> bool:
        ...

    def plot(self: Self, data: pd.DataFrame, ticker: str, indicator_names: list[str]) -> None:
        subplots = self._gather_all_subplots(data, ticker, indicator_names)
        if len(subplots) == 0:
            self._plot_stock_price(data, ticker)
        else:
            self._plot_stock_price_with_indicator(data, ticker, indicator_names, subplots)
        plt.close()

    def _gather_all_subplots(self: Self, data: pd.DataFrame, ticker: str, indicator_names: list[str]) -> list[Subplot]:
        subplots: list[Subplot] = []
        for indicator_name in indicator_names:
            self._plot_indicator(data, ticker, indicator_name, subplots)
        return subplots

    def _plot_stock_price(self: Self, data: pd.DataFrame, ticker: str) -> None:
        filename = self._get_file_name(ticker, [])
        mpf.plot(
            data[["Open", "High", "Low", "Close", "Volume"]],
            type="candle",
            style="yahoo",
            volume=True,
            savefig=filename
        )
        plt.close()

    def _plot_stock_price_with_indicator(
        self: Self,
        data: pd.DataFrame,
        ticker: str,
        indicator_names: list[str],
        subplots: list,
    ) -> None:
        try:
            mpf.plot(
                data[["Open", "High", "Low", "Close", "Volume"]],
                type="candle",
                style="yahoo",
                title=self._get_plot_name(ticker, indicator_names),
                addplot=subplots,
                volume=True,
                volume_panel=2,
                figratio=(6, 5),
                panel_ratios=(3, 4, 1),
                savefig=self._get_file_name(ticker, indicator_names)
            )
        except IndexError as e:
            print(f"Index Error for {ticker} - {len(data)} rows")
            raise e

    def _get_plot_name(self: Self, ticker: str, indicator_names: list[str]) -> str:
        return f"{ticker}: {indicator_names[0] if len(indicator_names) > 0 else 'stock prices'}"

    def _get_file_name(self: Self, ticker: str, indicator_names: list[str]) -> str:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        return APP_SETTINGS.report_output_path / f"{ticker}_{'_'.join(indicator_names)}_{timestamp}.png"
    
    def _plot_indicator(self: Self, data: pd.DataFrame, ticker: str, indicator_name: str, subplots: list) -> None:
        if self._can_draw_indicator(indicator_name):
            subplots.append(self._get_subplot(data, indicator_name))
        elif self._next_visualizer is not None:
            self._next_visualizer._plot_indicator(data, ticker, indicator_name, subplots)

    @abstractmethod
    def _get_subplot(self: Self, data: pd.DataFrame, indicator_name: str) -> Subplot:
        ...


class RSIVisualizer(Visualizer):
    def _can_draw_indicator(self: Self, indicator_name: str) -> bool:
        return indicator_name.startswith("RSI")

    def _get_subplot(self: Self, data: pd.DataFrame, indicator_name: str) -> Subplot:
        return mpf.make_addplot(data[indicator_name], panel=1, ylabel=indicator_name)


class MACDVisualizer(Visualizer):
    def _can_draw_indicator(self: Self, indicator_name: str) -> bool:
        return indicator_name in ["MACDLine", "SignalLine", "MACDHistogram"]

    def _get_subplot(self: Self, data: pd.DataFrame, indicator_name: str) -> Subplot:
        if indicator_name == "MACDHistogram":
            return mpf.make_addplot(
                data["MACDHistogram"],
                type="bar",
                width=0.7,
                panel=1,
                color="dimgray",
                alpha=1,
                secondary_y=True,
            )
        elif indicator_name == "MACDLine":
            return mpf.make_addplot(data["MACDLine"], panel=1, color="fuchsia", secondary_y=False)
        elif indicator_name == "SignalLine":
            return mpf.make_addplot(data["SignalLine"], panel=1, color="b", secondary_y=False)
        raise ValueError(f"MACDVisualizer: Unsupported indicator name: {indicator_name}")


class SimpleMovingAverageVisualizer(Visualizer):
    def _can_draw_indicator(self: Self, indicator_name: str) -> bool:
        return indicator_name.startswith("SMA")

    def _get_subplot(self: Self, data: pd.DataFrame, indicator_name: str) -> Subplot:
        color = "green" if "200" in indicator_name else "blue"
        return mpf.make_addplot(data[indicator_name], panel=1, color=color)


class ExponentialMovingAverageVisualizer(Visualizer):
    def _can_draw_indicator(self: Self, indicator_name: str) -> bool:
        return indicator_name.startswith("EMA")

    def _get_subplot(self: Self, data: pd.DataFrame, indicator_name: str) -> Subplot:
        color = "lime" if "12" in indicator_name else "c"
        return mpf.make_addplot(data[indicator_name], panel=1, color=color)
