from typing import Self

import pandas as pd

from acquisition.data_loaders.data_loader import DataLoader
from reporting.visualizer import Visualizer
from utils.date_range import DateRange
from trading_algorithms.factory import IndicatorFactory


class PlottingWorkflow:
    def __init__(
        self: Self,
        tickers: list[str],
        data_loader: DataLoader,
        visualizer: Visualizer,
        indicator_factory: IndicatorFactory,
    ) -> None:
        self._tickers = tickers
        self._data_loader = data_loader
        self._visualizer = visualizer
        self._indicator_factory = indicator_factory

    def plot(self: Self, indicator: str, date_range: DateRange) -> None:
        data = self._data_loader.load_for_tickers(self._tickers, date_range)
        for ticker in self._tickers:
            self._plot_for_ticket(data[ticker], ticker, indicator)

    def _plot_for_ticket(
        self: Self, ticker_ohlc: pd.DataFrame, ticker: str, indicator_name: str
    ) -> None:
        indicator_columns = []
        if indicator_name.upper() != "RAW":
            indicator = self._indicator_factory(indicator_name)
            indicator.compute(ticker_ohlc)
            indicator_columns = indicator.columns_for_plot
        self._visualizer.plot(ticker_ohlc, ticker, indicator_columns)
