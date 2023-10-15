import pytest
from simulation.portfolio_manager import PortfolioManager, PortfolioException


def test_buy() -> None:
    manager = PortfolioManager()
    manager.recapitalize(1000.0)
    manager.buy("AAPL", 100.0, 5)
    summary = manager.summary({"AAPL": 100.0})
    assert summary["cash"] == 500.0
    assert summary["stocks"] == {"AAPL": 5}

    with pytest.raises(PortfolioException):
        manager.buy("AAPL", 200.0, 10)


def test_buy_with_entire_cash() -> None:
    manager = PortfolioManager()
    manager.recapitalize(1000.0)
    manager.buy_with_entire_cash("AAPL", 100.0)
    summary = manager.summary({"AAPL": 100.0})
    assert summary["cash"] == 0.0
    assert summary["stocks"] == {"AAPL": 10}

    manager.recapitalize(1000.0)
    manager.buy_with_entire_cash("AAPL", 200.0)
    summary = manager.summary({"AAPL": 200.0})
    assert summary["cash"] == 0.0
    assert summary["stocks"] == {"AAPL": 15}

    with pytest.raises(PortfolioException):
        manager.buy_with_entire_cash("AAPL", 1500.0)


def test_sell() -> None:
    manager = PortfolioManager()
    manager.recapitalize(1000.0)
    manager.buy("AAPL", 100.0, 5)
    manager.sell("AAPL", 200.0, 2)
    summary = manager.summary({"AAPL": 200.0})
    assert summary["cash"] == 900.0
    assert summary["stocks"] == {"AAPL": 3}

    with pytest.raises(PortfolioException):
        manager.sell("AAPL", 200.0, 10)

    with pytest.raises(PortfolioException):
        manager.sell("GOOG", 200.0, 2)


def test_sell_all() -> None:
    manager = PortfolioManager()
    manager.recapitalize(1000.0)
    manager.buy("AAPL", 100.0, 5)
    manager.sell_all("AAPL", 200.0)
    summary = manager.summary({"AAPL": 200.0})
    assert summary["cash"] == 1500.0
    assert summary["stocks"] == {}

    with pytest.raises(PortfolioException):
        manager.sell_all("AAPL", 200.0)

    with pytest.raises(PortfolioException):
        manager.sell_all("GOOG", 200.0)


def test_get_value() -> None:
    manager = PortfolioManager()
    manager.recapitalize(1000.0)
    manager.buy("AAPL", 100.0, 4)
    manager.buy("GOOG", 200.0, 3)
    assert manager.get_value({"AAPL": 150.0, "GOOG": 250.0}) == 1350.0


def test_summary() -> None:
    manager = PortfolioManager()
    manager.recapitalize(1000.0)
    manager.buy("AAPL", 100.0, 4)
    manager.buy("GOOG", 200.0, 3)
    assert manager.summary({"AAPL": 150.0, "GOOG": 250.0}) == {
        "stocks": {"AAPL": 4, "GOOG": 3},
        "cash": 0.0,
        "total_value": 1350.0,
    }


def test_owns() -> None:
    manager = PortfolioManager()
    manager.recapitalize(1000.0)
    manager.buy("AAPL", 100.0, 5)
    assert manager.owns("AAPL")
    assert not manager.owns("GOOG")
