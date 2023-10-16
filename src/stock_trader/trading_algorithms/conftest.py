import pandas as pd
from pathlib import Path
import pytest


@pytest.fixture
def sample_data_from_file() -> pd.DataFrame:
    path = Path(__file__).parent / "test_data/aapl.us.txt"
    return pd.read_csv(path)
