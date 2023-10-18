from abc import ABC, abstractmethod
from concurrent.futures import ProcessPoolExecutor, as_completed
import math
from typing import Self

import pandas as pd

from stock_trader.reporting.visualizer import Visualizer
from stock_trader.settings import APP_SETTINGS


class VisualizerRunner(ABC):
    
    @abstractmethod
    def plot(self: Self, data: dict[str, pd.DataFrame], tickers: list[str], indicator_names: list[str]) -> None:
        ...

class SingleThreadedVisualizerRunner(VisualizerRunner):
    def __init__(self: Self, visualizer: Visualizer) -> None:
        self._visualizer = visualizer

    def plot(self: Self, data: dict[str, pd.DataFrame], tickers: list[str], indicator_names: list[str]) -> None:
        for ticker in tickers:
            self._visualizer.plot(data[ticker], ticker, indicator_names)


class NaiveMultiprocessingVisualizerRunner(VisualizerRunner):
    def __init__(self: Self, visualizer: Visualizer) -> None:
        self._visualizer = visualizer

    def plot(self: Self, data: dict[str, pd.DataFrame], tickers: list[str], indicator_names: list[str]) -> None:
        with ProcessPoolExecutor(max_workers=APP_SETTINGS.num_workers) as executor:
            futures = [executor.submit(self._visualizer.plot, data[ticker], ticker, indicator_names) for ticker in tickers]
            left = len(futures)
            for future in as_completed(futures):
                left -= 1
                future.add_done_callback(lambda _: print(f"Done - {left} left of {len(futures)}"))

class ChunkedMultiprocessingVisualizerRunner(VisualizerRunner):
    def __init__(self: Self, visualizer: Visualizer) -> None:
        self._visualizer = visualizer

    def plot(self: Self, data: dict[str, pd.DataFrame], tickers: list[str], indicator_names: list[str]) -> None:
        with ProcessPoolExecutor(max_workers=APP_SETTINGS.num_workers) as executor:
            chunk_size = math.ceil(len(tickers) / APP_SETTINGS.num_workers)
            ticker_chunks = [tickers[i: i + chunk_size] for i in range(APP_SETTINGS.num_workers)]
            data_chunks = [{ticker: data[ticker] for ticker in chunk} for chunk in ticker_chunks]
            runner = SingleThreadedVisualizerRunner(self._visualizer)
            futures = []
            for ticker_chunk, data_chunk in zip(ticker_chunks, data_chunks):
                futures.append(executor.submit(runner.plot, data_chunk, ticker_chunk, indicator_names))
            left = len(futures)
            for future in as_completed(futures):
                left -= 1
                future.add_done_callback(lambda _: print(f"Done - {left} left of {len(futures)} futures"))