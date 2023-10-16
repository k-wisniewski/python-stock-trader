from datetime import datetime
from pathlib import Path
import pandas as pd
import pytest
from stock_trader.acquisition.data_sources.alpha_vantage import AlphaVantageDataSource
from stock_trader.acquisition.data_sources.data_source import DataSource

from stock_trader.acquisition.data_sources.local_csv import LocalCSVDataSource, TickerNotFoundError
from stock_trader.acquisition.data_sources.yahoo_finance import YFinanceDataSource
from stock_trader.utils.date_range import DateRange

FROZEN_TIME = "2017-11-09"
DATA_SOURCES = {
    LocalCSVDataSource(Path(__file__).parent / "test_data/"): DateRange(
        start=datetime(2007, 11, 9), end=datetime(2017, 11, 9)
    ),
    AlphaVantageDataSource("KMCTPR2AV0KNKXVX"): DateRange(start=datetime(2023, 7, 1), end=datetime(2023, 9, 20)),
    YFinanceDataSource(): DateRange(start=datetime(2023, 7, 1), end=datetime(2023, 9, 20)),
}

data_source_ids = [ds.__class__.__name__ for ds in DATA_SOURCES]


@pytest.mark.parametrize("data_source", DATA_SOURCES, ids=data_source_ids)
def test_correct_columns_are_returned(data_source: DataSource):
    df = data_source.fetch("ge", DateRange(start=datetime(2007, 11, 9), end=datetime(2017, 11, 9)))
    assert (df.columns == pd.Index(["Open", "High", "Low", "Close", "Volume"])).all()


@pytest.mark.parametrize("data_source", DATA_SOURCES, ids=data_source_ids)
def test_returns_maximum_available_range_of_data_when_date_range_larger(
    data_source: DataSource,
) -> None:
    date_range = DateRange(start=datetime(1900, 11, 9), end=datetime(2037, 11, 9))
    df = data_source.fetch("aapl", date_range)
    assert len(df) > 0
    assert df.index[0] >= date_range.start
    assert df.index[-1] <= date_range.end


@pytest.mark.parametrize("data_source", DATA_SOURCES, ids=data_source_ids)
def test_raises_TickerNotFound_when_ticker_not_found(data_source: DataSource) -> None:
    with pytest.raises(TickerNotFoundError):
        data_source.fetch("nvgasdasda", DateRange.years_back(10))
