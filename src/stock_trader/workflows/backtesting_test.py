# end to end tests for backtesting workflow
from datetime import datetime
from pathlib import Path
from freezegun import freeze_time

from pytest import MonkeyPatch
from stock_trader.acquisition.data_loaders.data_loader import SingleThreadedDataLoader
from stock_trader.acquisition.data_sources.data_source import DataSource
from stock_trader.settings import Settings
from stock_trader.trading_algorithms.signals import MovingAverageCrossoverSignal
from stock_trader.utils.date_range import DateRange
from stock_trader.workflows.backtesting import BacktestingWorkflow


@freeze_time("2021-01-01")
def test_backtesting_workflow(tmp_path: Path, fake_data_source: DataSource, monkeypatch: MonkeyPatch) -> None:
    settings = Settings(report_output_path=tmp_path)
    monkeypatch.setattr("stock_trader.reporting.generate_report.APP_SETTINGS", settings)
    tickers = ["GE", "AAPL"]
    date_range = DateRange(start=datetime(2021, 1, 1), end=datetime(2021, 1, 10))
    data_loader = SingleThreadedDataLoader(fake_data_source)
    workflow = BacktestingWorkflow(tickers, data_loader, MovingAverageCrossoverSignal())
    workflow.backtest(date_range, 10000)
    assert (tmp_path / Path("report_GE_2021-01-01_00-00-00.txt")).exists()
    assert (tmp_path / Path("report_AAPL_2021-01-01_00-00-00.txt")).exists()
    with open(tmp_path / Path("report_GE_2021-01-01_00-00-00.txt"), "r") as file:
        report = file.read()
        assert "Annualized Return" in report
        assert "Sharpe Ratio" in report
        assert "Maximum Drawdown" in report
