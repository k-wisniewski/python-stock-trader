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
    model_config = SettingsConfigDict(env_prefix="STOCK_TRADER_", env_file=Path(".env"), env_file_encoding="utf-8")
    report_output_path: DirectoryPath = DirectoryPath("reports")
    source_data_folder: DirectoryPath = DirectoryPath("data")
    concurrency: Concurrency = Concurrency.THREADS


APP_SETTINGS = Settings()
