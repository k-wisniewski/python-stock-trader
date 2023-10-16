from freezegun import freeze_time
import pytest
from datetime import datetime

from stock_trader.reporting.history import HistoryItem
from stock_trader.reporting.generate_report import create_report, save_report
from stock_trader.settings import Settings


@pytest.fixture
def history():
    return [
        HistoryItem(datetime(2021, 1, 1), 10.5),
        HistoryItem(datetime(2021, 1, 2), 11.2),
        HistoryItem(datetime(2021, 1, 3), 12.1),
        HistoryItem(datetime(2021, 1, 4), 11.8),
        HistoryItem(datetime(2021, 1, 5), 12.5),
        HistoryItem(datetime(2021, 1, 6), 13.2),
        HistoryItem(datetime(2021, 1, 7), 14.1),
        HistoryItem(datetime(2021, 1, 8), 13.8),
        HistoryItem(datetime(2021, 1, 9), 14.5),
        HistoryItem(datetime(2021, 1, 10), 15.2),
    ]


def test_create_report(history):
    report = create_report(history)
    assert isinstance(report, str)
    assert "Annualized Return" in report
    assert "Sharpe Ratio" in report
    assert "Maximum Drawdown" in report


@freeze_time("2021-01-01")
def test_save_report(history, tmp_path, monkeypatch):
    report = create_report(history)
    settings = Settings(report_output_path=tmp_path)
    monkeypatch.setattr("reporting.generate_report.APP_SETTINGS", settings)
    save_report(report, "GE")
    filename = f"report_GE_2021-01-01_00-00-00.txt"
    assert (tmp_path / filename).exists()
    with open(tmp_path / filename, "r") as file:
        report = file.read()
        assert isinstance(report, str)
        assert "Annualized Return" in report
        assert "Sharpe Ratio" in report
        assert "Maximum Drawdown" in report
