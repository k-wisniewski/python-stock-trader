import functools
from typing import Any, Self
import pandas as pd
from abc import ABCMeta, abstractmethod

from utils.date_range import DateRange


class TickerNotFoundError(Exception):
    ...


class DataSourceMeta(ABCMeta):
    def __init__(cls, name: str, bases: tuple[type, ...], attrs: dict[str, Any]):
        super().__init__(name, bases, attrs)
        if "fetch" in attrs and name != "DataSource":
            original_fetch = cls.fetch  # type: ignore

            @functools.wraps(original_fetch)
            def fetch_wrapper(*args, **kwargs) -> pd.DataFrame:  # type: ignore
                result = original_fetch(*args, **kwargs)

                if not isinstance(result, pd.DataFrame):
                    raise TypeError(f"{name}.fetch must return a pandas DataFrame")

                required_columns = {"Open", "High", "Low", "Close", "Volume"}
                if not required_columns.issubset(result.columns):
                    raise ValueError(
                        f"{name}.fetch must return a DataFrame with columns {required_columns}"
                    )

                return result

            setattr(cls, "fetch", fetch_wrapper)


class DataSource(metaclass=DataSourceMeta):
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
        self._drop_unwanted_cols(df)
        return df

    def _drop_unwanted_cols(self: Self, df: pd.DataFrame) -> None:
        desired_cols = {"Open", "High", "Low", "Close", "Volume"}
        for col in df.columns:
            if col not in desired_cols:
                df.drop(col, axis=1, inplace=True)

    def trim_to_data_range(
        self, date_range: DateRange, df: pd.DataFrame
    ) -> pd.DataFrame:
        return df[(df.index >= date_range.start) & (df.index <= date_range.end)]
