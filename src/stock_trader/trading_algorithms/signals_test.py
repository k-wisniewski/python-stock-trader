import pandas as pd

from stock_trader.trading_algorithms.signals import (
    MovingAverageConvergenceDivergenceSignal,
    MovingAverageCrossoverSignal,
    RelativeStrengthIndexSignal,
)


def test_moving_average_crossover(sample_data_from_file: pd.DataFrame) -> None:
    signal = MovingAverageCrossoverSignal()
    signal_column = signal.generate_signals(sample_data_from_file)
    assert signal_column == "Signal_EMA5_SMA200"
    for row in sample_data_from_file.itertuples():
        if row.SMA_200 >= row.EMA_5:
            assert row.Signal_EMA5_SMA200 == -1.0
        elif row.SMA_200 < row.EMA_5:
            assert row.Signal_EMA5_SMA200 == 1.0


def test_relative_strength_index(sample_data_from_file: pd.DataFrame) -> None:
    signal = RelativeStrengthIndexSignal()
    signal_column = signal.generate_signals(sample_data_from_file)
    assert signal_column == "Signal_RSI_14"
    for row in sample_data_from_file.iloc[14:].itertuples():
        if row.RSI_14 > 70:
            assert row.Signal_RSI_14 == -1.0
        elif row.RSI_14 < 30:
            assert row.Signal_RSI_14 == 1.0
        else:
            assert row.Signal_RSI_14 == 0.0


def test_macd_signal(sample_data_from_file: pd.DataFrame) -> None:
    signal = MovingAverageConvergenceDivergenceSignal()
    signal_column = signal.generate_signals(sample_data_from_file)
    assert signal_column == "Signal_MACD_12_26_9"
    for row in sample_data_from_file.itertuples():
        if row.MACDLine > row.SignalLine:
            assert row.Signal_MACD_12_26_9 == 1.0
        elif row.MACDLine < row.SignalLine:
            assert row.Signal_MACD_12_26_9 == -1.0
        else:
            assert row.Signal_MACD_12_26_9 == 0.0
