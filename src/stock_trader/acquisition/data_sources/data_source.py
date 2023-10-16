from typing import Self
import pandas as pd
from abc import ABC, abstractmethod

from stock_trader.utils.date_range import DateRange


class TickerNotFoundError(Exception):
    ...


class DataSource(ABC):
    def fetch(self: Self, ticker: str, date_range: DateRange) -> pd.DataFrame:
        df = self.load_to_dataframe(ticker)
        df = self.standardize_dataframe(df)
        return self.trim_to_data_range(date_range, df)

    @abstractmethod
    def load_to_dataframe(self: Self, ticker: str) -> pd.DataFrame:
        ...

    def standardize_dataframe(self: Self, df: pd.DataFrame) -> pd.DataFrame:
        df.dropna(inplace=True)
        df.sort_index(inplace=True)
        return df

    def trim_to_data_range(self, date_range: DateRange, df: pd.DataFrame) -> pd.DataFrame:
        return df[(df.index >= date_range.start) & (df.index <= date_range.end)]
