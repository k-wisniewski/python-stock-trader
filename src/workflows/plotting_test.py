from datetime import datetime
from pathlib import Path
from freezegun import freeze_time
import pytest
from acquisition.data_loaders.data_loader_factory import data_loader_factory
from acquisition.data_sources.data_source_factory import Source, data_source_factory

from reporting.visualizer_factory import visualizer_factory
from settings import Concurrency
from trading_algorithms.factory import indicator_factory
from utils.date_range import DateRange
from workflows.plotting import PlottingWorkflow


@freeze_time("2020-01-01")
def test_plotting_workflow(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "reporting.visualizer.APP_SETTINGS.report_output_path", tmp_path
    )
    monkeypatch.setattr(
        "acquisition.data_loaders.data_loader_factory.APP_SETTINGS.concurrency",
        Concurrency.SINGLE_THREADED,
    )
    tickers = ["AAPL"]
    data_loader = data_loader_factory(data_source_factory(Source.LOCAL))
    visualizer = visualizer_factory()
    workflow = PlottingWorkflow(tickers, data_loader, visualizer, indicator_factory)
    date_range = DateRange(
        start=datetime(year=2010, month=1, day=1),
        end=datetime(year=2010, month=5, day=5),
    )
    workflow.plot("RSI_14", date_range)
    assert (tmp_path / Path("AAPL_RSI_14_2020-01-01_00-00-00.png")).exists()
