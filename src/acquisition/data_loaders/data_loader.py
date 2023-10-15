from abc import ABC, abstractmethod
from concurrent.futures import Executor, as_completed
from typing import Self, Type

import pandas as pd
from acquisition.data_sources.data_source import DataSource

from utils.date_range import DateRange


class DataLoader(ABC):
    @abstractmethod
    def load_for_tickers(
        self: Self, tickers: list[str], date_range: DateRange
    ) -> dict[str, pd.DataFrame]:
        ...


class SingleThreadedDataLoader(DataLoader):
    def __init__(self: Self, data_source: DataSource) -> None:
        self._data_source = data_source

    def load_for_tickers(
        self: Self, tickers: list[str], date_range: DateRange
    ) -> dict[str, pd.DataFrame]:
        return {
            ticker: self._data_source.fetch(ticker, date_range) for ticker in tickers
        }


class ParallelDataLoader(DataLoader):
    def __init__(
        self: Self,
        data_source: DataSource,
        num_workers: int,
        executor_cls: Type[Executor],
    ) -> None:
        self._data_source = data_source
        self._num_workers = num_workers
        self._executor_cls = executor_cls

    def load_for_tickers(
        self: Self, tickers: list[str], date_range: DateRange
    ) -> dict[str, pd.DataFrame]:
        result = {}
        # both ThreadPoolExecutor and ProcessPoolExecutor have max_workers
        with self._executor_cls(max_workers=self._num_workers) as executor:  # type: ignore
            futures = {
                executor.submit(self._data_source.fetch, ticker, date_range): ticker
                for ticker in tickers
            }
            for future in as_completed(futures):
                result[futures[future]] = future.result()
        return result
