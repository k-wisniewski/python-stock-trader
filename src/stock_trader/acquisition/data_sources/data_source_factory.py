from enum import Enum, auto
from pathlib import Path
from src.stock_trader import settings
from src.stock_trader.acquisition.data_sources.alpha_vantage import AlphaVantageDataSource
from src.stock_trader.acquisition.data_sources.data_source import DataSource
from src.stock_trader.acquisition.data_sources.local_csv import LocalCSVDataSource
from src.stock_trader.acquisition.data_sources.yahoo_finance import YFinanceDataSource


class Source(Enum):
    ALPHA_VANTAGE = auto()
    YFINANCE = auto()
    LOCAL = auto()


def data_source_factory(
    source: Source,
    alpha_vantage_api_key: str | None = None,
    data_folder: Path | None = None,
) -> DataSource:
    if source == Source.ALPHA_VANTAGE and alpha_vantage_api_key is not None:
        return AlphaVantageDataSource(alpha_vantage_api_key or settings.APP_SETTINGS.alpha_vantage_api_key)
    elif source == Source.LOCAL:
        return LocalCSVDataSource(data_folder)
    elif source == Source.YFINANCE:
        return YFinanceDataSource()
    raise RuntimeError("invalid parameters to data source factory")
