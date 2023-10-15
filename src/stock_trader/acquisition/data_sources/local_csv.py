from math import e
from pathlib import Path
from typing import Self
import pandas as pd
from stock_trader.acquisition.data_sources.data_source import DataSource, TickerNotFoundError
from stock_trader.settings import APP_SETTINGS


class LocalCSVDataSource(DataSource):
    def __init__(self: Self, data_folder: Path | None = None) -> None:
        self._data_folder = data_folder or APP_SETTINGS.source_data_folder

    def load_to_dataframe(self: Self, ticker: str) -> pd.DataFrame:
        try:
            file_name = f"{ticker.lower()}.us.txt"
            return pd.read_csv(self._data_folder / file_name, parse_dates=True, index_col=0)
        except FileNotFoundError as e:
            raise TickerNotFoundError() from e

    def __str__(self) -> str:
        return "LocalCSV"
