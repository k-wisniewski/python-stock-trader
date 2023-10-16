from datetime import datetime
from pathlib import Path
from freezegun import freeze_time
import pytest
from stock_trader.acquisition.data_loaders.data_loader_factory import data_loader_factory
from stock_trader.acquisition.data_sources.data_source_factory import Source, data_source_factory
from stock_trader.reporting.visualizer import Visualizer

from stock_trader.settings import Concurrency
from stock_trader.trading_algorithms.factory import indicator_factory
from stock_trader.utils.date_range import DateRange
from stock_trader.workflows.plotting import PlottingWorkflow


@freeze_time("2020-01-01")
def test_plotting_workflow(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("stock_trader.reporting.visualizer.APP_SETTINGS.report_output_path", tmp_path)
    monkeypatch.setattr(
        "stock_trader.acquisition.data_loaders.data_loader_factory.APP_SETTINGS.concurrency",
        Concurrency.SINGLE_THREADED,
    )
    tickers = ["AAPL"]
    data_loader = data_loader_factory(data_source_factory(Source.LOCAL))
    visualizer = Visualizer()
    workflow = PlottingWorkflow(tickers, data_loader, visualizer, indicator_factory)
    date_range = DateRange(
        start=datetime(year=2010, month=1, day=1),
        end=datetime(year=2010, month=5, day=5),
    )
    workflow.plot("RSI_14", date_range)
    assert (tmp_path / Path("AAPL_RSI_14_2020-01-01_00-00-00.png")).exists()
