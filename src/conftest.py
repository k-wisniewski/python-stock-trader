from typing import Self
import pandas as pd
import pytest

from acquisition.data_sources.data_source import DataSource
from utils.date_range import DateRange


class FakeDataSource(DataSource):
    def fetch(self: Self, ticker: str, date_range: DateRange) -> pd.DataFrame:
        df = self.load_to_dataframe(ticker)
        date_range_series = pd.date_range(start="2023-01-01", periods=len(df), freq="D")
        df.set_index(date_range_series, inplace=True)
        return df

    def load_to_dataframe(self, _: str) -> pd.DataFrame:
        return pd.DataFrame(
            {
                "Open": [24.333, 25.123, 26.234, 27.345, 28.456],
                "High": [24.333, 25.123, 26.234, 27.345, 28.456],
                "Low": [23.946, 24.567, 25.678, 26.789, 27.890],
                "Close": [23.946, 24.567, 25.678, 26.789, 27.890],
                "Volume": [68847968, 69847968, 70847968, 71847968, 72847968],
            },
            index=pd.date_range(start="2020-01-01", periods=5, freq="D"),
        )


@pytest.fixture()
def fake_data_source():
    return FakeDataSource()
