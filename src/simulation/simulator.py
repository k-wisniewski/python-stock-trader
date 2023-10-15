from typing import Self
import pandas as pd
from reporting.history import History, HistoryItem
from simulation.portfolio_manager import PortfolioException, PortfolioManager
from trading_algorithms.signals import Signal


class TradingSimulator:
    def __init__(self, signal: Signal, portfolioManager: PortfolioManager):
        self._portfolio = portfolioManager
        self._history: History = []
        self._signal = signal

    def simulate(
        self: Self, data: pd.DataFrame, ticker: str, initial_capital: float = 10000.0
    ) -> None:
        self._portfolio.recapitalize(initial_capital)
        signal_column = self._signal.generate_signals(data)

        for index, row in data.iterrows():
            current_price = row["Close"]
            try:
                if row[signal_column] == 1.0:  # Buy signal
                    self._portfolio.buy_with_entire_cash(ticker, current_price)
                elif row[signal_column] == -1.0:  # Sell signal
                    self._portfolio.sell_all(ticker, current_price)
            except PortfolioException as e:
                print(e)
                continue
            current_value = self._portfolio.get_value({ticker: current_price})
            self._history.append(HistoryItem(str(index), current_value))

    @property
    def history(self: Self) -> History:
        return self._history
