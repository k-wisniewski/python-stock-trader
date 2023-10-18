from typing import Self

import pandas as pd

from stock_trader.acquisition.data_loaders.data_loader import DataLoader
from stock_trader.reporting.visualizer_runner import VisualizerRunner
from stock_trader.utils.date_range import DateRange
from stock_trader.trading_algorithms.factory import IndicatorFactory


class PlottingWorkflow:
    def __init__(
        self: Self,
        tickers: list[str],
        data_loader: DataLoader,
        visualizer_runner: VisualizerRunner,
        indicator_factory: IndicatorFactory,
    ) -> None:
        self._tickers = tickers
        self._data_loader = data_loader
        self._visualizer_runner = visualizer_runner
        self._indicator_factory = indicator_factory

    def plot(self: Self, indicator_name: str, date_range: DateRange) -> None:
        data = self._data_loader.load_for_tickers(self._tickers, date_range)
        tickers_with_data = [ticker for ticker in data.keys() if len(data[ticker]) > 0]
        indicator_columns = []
        for ticker in tickers_with_data:
            if indicator_name.upper() != "RAW":
                indicator = self._indicator_factory(indicator_name)
                indicator.compute(data[ticker])
                indicator_columns = indicator.columns_for_plot
        self._visualizer_runner.plot(data, tickers_with_data, indicator_columns)

