import pandas as pd
import pytest
from src.stock_trader.trading_algorithms.indicators import (
    ExponentialMovingAverage,
    SimpleMovingAverage,
    RelativeStrengthIndex,
    MovingAverageConvergenceDivergence,
)


@pytest.fixture
def sample_data() -> pd.DataFrame:
    opens = [
        100.0,
        101.3,
        102.0,
        102.5,
        101.0,
        99.84,
        103.0,
        104.2,
        104.1,
        104.7,
        105.1,
        106.0,
        106.2,
        103.1,
    ]
    highs = [
        100.57,
        101.42,
        102.65,
        103.20,
        101.04,
        100.52,
        103.27,
        105.10,
        104.66,
        104.89,
        105.83,
        106.84,
        106.69,
        103.11,
    ]
    lows = [
        99.05,
        100.77,
        101.79,
        101.02,
        99.29,
        98.44,
        102.43,
        103.65,
        102.77,
        103.18,
        103.77,
        104.27,
        105.29,
        101.97,
    ]
    closes = [
        99.99,
        101.26,
        101.96,
        102.30,
        101.03,
        98.83,
        102.88,
        103.90,
        103.34,
        103.43,
        104.81,
        106.75,
        105.58,
        102.31,
    ]
    volumes = [
        2147,
        3897,
        6305,
        8371,
        5141,
        4480,
        8768,
        2831,
        8830,
        8939,
        2576,
        8009,
        7435,
        9402,
    ]
    data = pd.DataFrame(
        {
            "Date": [
                "2021-01-01",
                "2021-01-02",
                "2021-01-03",
                "2021-01-04",
                "2021-01-05",
                "2021-01-06",
                "2021-01-07",
                "2021-01-08",
                "2021-01-09",
                "2021-01-10",
                "2021-01-11",
                "2021-01-12",
                "2021-01-13",
                "2021-01-14",
            ],
            "Open": opens,
            "High": highs,
            "Low": lows,
            "Close": closes,
            "Volume": volumes,
        }
    )
    return data


@pytest.mark.parametrize(
    "window_size,expected_ma",
    [(2, 103.945), (7, 104.30285714285715), (14, 102.74071428571428)],
)
def test_simple_moving_average_when_enough_data_for_window_size(
    sample_data: pd.DataFrame, window_size: int, expected_ma: float
) -> None:
    ma = SimpleMovingAverage(window_size=window_size)
    sma_columns = ma.compute(sample_data)
    assert sma_columns == [f"SMA_{window_size}"]
    assert sma_columns[0] in sample_data.columns
    assert sample_data[sma_columns[0]].iloc[-1] == pytest.approx(expected_ma, rel=1e-3)


def test_simple_moving_average_when_window_too_long(sample_data: pd.DataFrame) -> None:
    ma = SimpleMovingAverage(window_size=15)
    sma_columns = ma.compute(sample_data)
    assert sma_columns == ["SMA_15"]
    assert sma_columns[0] in sample_data.columns
    assert pd.isna(sample_data[sma_columns[0]].iloc[-1])


def test_exponential_moving_average(sample_data: pd.DataFrame) -> None:
    ma = ExponentialMovingAverage(window_size=2)
    ema_columns = ma.compute(sample_data)
    assert ema_columns == ["EMA_2"]
    assert ema_columns[0] in sample_data.columns
    assert sample_data[ema_columns[0]].iloc[-1] == pytest.approx(104.04, rel=1e-3)


def test_rsi_strategy(sample_data: pd.DataFrame) -> None:
    rsi = RelativeStrengthIndex(window_size=2)
    rsi_columns = rsi.compute(sample_data)
    assert rsi_columns == ["RSI_2"]
    assert rsi_columns[0] in sample_data.columns
    assert sample_data[rsi_columns[0]].iloc[-2] == pytest.approx(53.71, rel=1e-3)
    assert sample_data[rsi_columns[0]].iloc[-1] == pytest.approx(15.49, rel=1e-3)


def test_macd_strategy(sample_data_from_file: pd.DataFrame) -> None:
    macd = MovingAverageConvergenceDivergence()
    macd_columns = macd.compute(sample_data_from_file)
    assert macd_columns == ["MACDLine", "SignalLine", "MACDHistogram"]
    assert macd_columns[0] in sample_data_from_file.columns
    assert macd_columns[1] in sample_data_from_file.columns
    assert macd_columns[2] in sample_data_from_file.columns
    assert sample_data_from_file[macd_columns[0]].iloc[-1] == pytest.approx(4.979, rel=1e-3)
    assert sample_data_from_file[macd_columns[1]].iloc[-1] == pytest.approx(3.694, rel=1e-3)
    assert sample_data_from_file[macd_columns[2]].iloc[-1] == pytest.approx(1.284, rel=1e-3)
