from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from typing import Callable

from src.stock_trader.acquisition.data_loaders.data_loader import (
    DataLoader,
    ParallelDataLoader,
    SingleThreadedDataLoader,
)
from src.stock_trader.acquisition.data_sources.data_source import DataSource
from src.stock_trader.settings import APP_SETTINGS, Concurrency


def data_loader_factory(data_source: DataSource) -> DataLoader:
    concurrency = APP_SETTINGS.concurrency
    if concurrency == Concurrency.SINGLE_THREADED:
        return SingleThreadedDataLoader(data_source)
    elif concurrency == Concurrency.THREADS:
        return ParallelDataLoader(data_source, 4, ThreadPoolExecutor)
    elif concurrency == Concurrency.PROCESSESS:
        return ParallelDataLoader(data_source, 4, ProcessPoolExecutor)
    # TODO: handle AsyncIO
    raise ValueError("unsupported concurrency type")


DataLoaderFactory = Callable[[DataSource], DataLoader]
