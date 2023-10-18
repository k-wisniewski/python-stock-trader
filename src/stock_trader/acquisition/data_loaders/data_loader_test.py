from concurrent.futures import Executor, ProcessPoolExecutor, ThreadPoolExecutor
from datetime import datetime, timedelta
from pandas import Index
import pytest
from stock_trader.acquisition.data_loaders.data_loader import (
    ParallelDataLoader,
    SingleThreadedDataLoader,
)
from stock_trader.acquisition.data_sources.data_source import DataSource
from stock_trader.utils.date_range import DateRange

THREEE_DAYS_BACK = DateRange(start=datetime.now() - timedelta(days=3), end=datetime.now())

def test_single_threaded_data_loader_loads_data_for_each_ticker(
    fake_data_source: DataSource,
):
    loader = SingleThreadedDataLoader(fake_data_source)
    data = loader.load_for_tickers(["a"], THREEE_DAYS_BACK)
    assert data is not None
    assert "a" in data
    assert (data["a"].columns == Index(["Open", "High", "Low", "Close", "Volume"], dtype="object")).all()


@pytest.mark.parametrize("executor", [ThreadPoolExecutor, ProcessPoolExecutor])
def test_parallel_data_loader_loads_data_for_each_ticker(fake_data_source: DataSource, executor: type[Executor]):
    loader = ParallelDataLoader(fake_data_source, num_workers=2, executor_cls=executor)
    data = loader.load_for_tickers(["AAPL", "GOOG"], THREEE_DAYS_BACK)
    assert data is not None
    assert "AAPL" in data
    assert "GOOG" in data
    expected_columns: Index = Index(["Open", "High", "Low", "Close", "Volume"], dtype="object")
    for ticker_data in data.values():
        assert (ticker_data.columns == expected_columns).all()
