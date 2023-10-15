from enum import Enum, auto
from pydantic import DirectoryPath
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
import sys


class Concurrency(Enum):
    THREADS = auto()
    PROCESSESS = auto()
    ASYNCIO = auto()
    SINGLE_THREADED = auto()

ENV_FILE = Path(__file__).parent / ".env_run"
if "pytest" in sys.modules:
    ENV_FILE = Path(__file__).parent / ".env_test"
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="STOCK_TRADER_", env_file=ENV_FILE, env_file_encoding="utf-8")
    report_output_path: DirectoryPath
    source_data_folder: DirectoryPath
    alpha_vantage_api_key: str
    concurrency: Concurrency = Concurrency.SINGLE_THREADED

APP_SETTINGS = Settings()
