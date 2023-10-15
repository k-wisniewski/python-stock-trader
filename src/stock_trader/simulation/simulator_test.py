import pandas as pd
import pytest
from src.stock_trader.simulation.simulator import TradingSimulator
from src.stock_trader.simulation.portfolio_manager import PortfolioException, PortfolioManager
from src.stock_trader.trading_algorithms.signals import Signal


class FakeSignal(Signal):
    def generate_signals(self, data: pd.DataFrame) -> str:
        column = "FakeSignal"
        data.loc[data.index == "2022-01-01", column] = 0.0
        data.loc[data.index == "2022-01-02", column] = 1.0
        data.loc[data.index == "2022-01-03", column] = 0.0
        data.loc[data.index == "2022-01-04", column] = -1.0
        data.loc[data.index == "2022-01-05", column] = 0.0
        return column


@pytest.fixture
def signal():
    return FakeSignal()


@pytest.fixture
def data():
    return pd.DataFrame(
        {
            "Open": [100, 110, 120, 130, 140],
            "High": [105, 115, 125, 135, 145],
            "Low": [95, 105, 115, 125, 135],
            "Close": [102, 112, 122, 132, 142],
        },
        index=pd.date_range("2022-01-01", periods=5),
    )


@pytest.fixture
def portfolio_manager():
    return PortfolioManager()


@pytest.fixture
def trading_simulator(portfolio_manager: PortfolioManager, signal: Signal):
    return TradingSimulator(signal, portfolio_manager)


def test_simulator_buy_sell(data: pd.DataFrame, trading_simulator: TradingSimulator):
    # Test if the simulator can buy and sell correctly based on the signal
    trading_simulator.simulate(data, "AAPL", initial_capital=10000.0)

    # Check if the portfolio value is correct after each transaction
    assert trading_simulator.history[0].value == 10000.0
    assert trading_simulator.history[1].value == 10000.0
    assert trading_simulator.history[2].value == 10890.0
    assert trading_simulator.history[3].value == 11780.0
    assert trading_simulator.history[4].value == 11780.0


def test_simulator_no_capital(data: pd.DataFrame, trading_simulator: TradingSimulator):
    # Test if the simulator can handle a zero initial capital
    trading_simulator.simulate(data, "AAPL", initial_capital=0.0)

    # Check if the portfolio value remains zero throughout the simulation
    assert all(item.value == 0.0 for item in trading_simulator.history)
