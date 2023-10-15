from enum import Enum, auto
from pydantic import DirectoryPath
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Concurrency(Enum):
    THREADS = auto()
    PROCESSESS = auto()
    ASYNCIO = auto()
    SINGLE_THREADED = auto()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="STOCK_TRADING_")
    report_output_path: DirectoryPath = Path(__file__).parents[1] / DirectoryPath(
        "reports"
    )
    source_data_folder: DirectoryPath = Path(__file__).parents[1] / DirectoryPath(
        "data"
    )
    concurrency: Concurrency = Concurrency.THREADS


APP_SETTINGS = Settings()
