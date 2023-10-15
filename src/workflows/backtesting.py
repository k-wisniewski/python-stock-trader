from typing import Self
from acquisition.data_loaders.data_loader import DataLoader
from reporting.generate_report import create_report, save_report
from simulation.portfolio_manager import PortfolioManager
from simulation.simulator import TradingSimulator
from trading_algorithms.signals import Signal
from utils.date_range import DateRange

import pandas as pd


class BacktestingWorkflow:
    def __init__(
        self: Self, tickers: list[str], data_loader: DataLoader, signal: Signal
    ) -> None:
        self._data_loader = data_loader
        self._tickers = tickers
        self._signal = signal

    def backtest(self: Self, date_range: DateRange, initial_lump_sum: float) -> None:
        data = self._data_loader.load_for_tickers(self._tickers, date_range)
        for ticker in self._tickers:
            self._backtest_single_ticker(data[ticker], initial_lump_sum, ticker)

    def _backtest_single_ticker(
        self, data: pd.DataFrame, initial_lump_sum: float, ticker: str
    ) -> None:
        simulator = TradingSimulator(self._signal, PortfolioManager())
        simulator.simulate(data, ticker, initial_lump_sum)
        report = create_report(simulator.history)
        save_report(report, ticker)
