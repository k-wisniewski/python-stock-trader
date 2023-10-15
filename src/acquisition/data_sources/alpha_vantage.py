from typing import Any, Self, cast

from acquisition.data_sources.data_source import DataSource, TickerNotFoundError
import requests
import pandas as pd


class AlphaVantageDataSource(DataSource):
    def __init__(self: Self, api_key: str) -> None:
        self.__API_KEY = api_key

    def standardize_dataframe(self: Self, df: pd.DataFrame) -> pd.DataFrame:
        df.columns = self._rename_columns(df)
        df.index = self._convert_index(df)
        super().standardize_dataframe(df)
        self._convert_columns(df)
        return df

    def load_to_dataframe(self: Self, ticker: str) -> pd.DataFrame:
        raw_data = self._fetch_raw_data(ticker)
        df = self._make_dataframe_from_raw_data(raw_data)
        return df

    def _make_dataframe_from_raw_data(
        self: Self, raw_data: dict[str, Any]
    ) -> pd.DataFrame:
        return pd.DataFrame.from_dict(raw_data["Time Series (Daily)"], orient="index")

    def _fetch_raw_data(self: Self, ticker: str) -> dict[str, Any]:
        r = requests.get(
            f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={self.__API_KEY}"
        )
        raw_data = r.json()
        # TODO: Handle throttling
        if "Error Message" in raw_data:
            raise TickerNotFoundError()
        return cast(dict[str, Any], raw_data)

    def _convert_columns(self: Self, df: pd.DataFrame) -> None:
        for col in df.columns:
            df[col] = pd.to_numeric(df[col])

    def _convert_index(self: Self, df: pd.DataFrame) -> pd.DatetimeIndex:
        return pd.to_datetime(df.index)

    def _rename_columns(self: Self, df: pd.DataFrame) -> pd.Index: # type: ignore
        return pd.Index([col.split(". ")[1].capitalize() for col in df.columns])

    def __str__(self: Self) -> str:
        return "AlphaVantage"
