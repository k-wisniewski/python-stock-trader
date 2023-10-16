# tests for Visualizer's subclassess
from pathlib import Path
from freezegun import freeze_time
import pandas as pd
import pytest
from stock_trader.acquisition.data_sources.data_source import DataSource
from stock_trader.reporting.visualizer import (
    ExponentialMovingAverageVisualizer,
    MACDVisualizer,
    RSIVisualizer,
    SimpleMovingAverageVisualizer,
)
from stock_trader.reporting.visualizer_factory import visualizer_factory


@freeze_time("2020-01-01")
def test_visualizer_outputs_png_image_in_the_report_output_path_for_just_stock_price(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, fake_data_source: DataSource
) -> None:
    visualizer = visualizer_factory()
    monkeypatch.setattr("reporting.visualizer.APP_SETTINGS.report_output_path", tmp_path)
    data = fake_data_source.load_to_dataframe("AAPL")
    visualizer.plot(data, "AAPL", [])
    assert (tmp_path / Path("AAPL__2020-01-01_00-00-00.png")).exists()


def test_visualizer_can_draw_rsi_plots() -> None:
    rsi_visualizer = RSIVisualizer()
    assert rsi_visualizer._can_draw_indicator("RSI")
    assert rsi_visualizer._can_draw_indicator("RSI_14")
    assert not rsi_visualizer._can_draw_indicator("MACDLine")


@freeze_time("2020-01-01")
def test_rsi_visualizer_outputs_png_image_in_the_report_output_path(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, fake_data_source: DataSource
) -> None:
    visualizer = visualizer_factory()
    monkeypatch.setattr("reporting.visualizer.APP_SETTINGS.report_output_path", tmp_path)
    data = fake_data_source.load_to_dataframe("AAPL")
    data["RSI_14"] = pd.Series([47.0, 31.0, 28.0, 37.0, 52.0], index=data.index, name="RSI_14")
    visualizer.plot(data, "AAPL", ["RSI_14"])
    assert (tmp_path / Path("AAPL_RSI_14_2020-01-01_00-00-00.png")).exists()


def test_visualizer_can_draw_macd_plots() -> None:
    visualizer = MACDVisualizer()
    assert visualizer._can_draw_indicator("MACDLine")
    assert visualizer._can_draw_indicator("SignalLine")
    assert visualizer._can_draw_indicator("MACDHistogram")


@freeze_time("2020-01-01")
def test_macd_visualizer_outputs_png_image_in_the_report_output_path(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, fake_data_source: DataSource
) -> None:
    visualizer = visualizer_factory()
    monkeypatch.setattr("reporting.visualizer.APP_SETTINGS.report_output_path", tmp_path)
    data = fake_data_source.load_to_dataframe("AAPL")
    data["MACDLine"] = pd.Series([47.0, 31.0, 28.0, 37.0, 52.0], index=data.index, name="MACDLine")
    data["SignalLine"] = pd.Series([47.0, 31.0, 28.0, 37.0, 52.0], index=data.index, name="SignalLine")
    data["MACDHistogram"] = pd.Series([47.0, 31.0, 28.0, 37.0, 52.0], index=data.index, name="MACDHistogram")
    visualizer.plot(data, "AAPL", ["MACDLine", "SignalLine", "MACDHistogram"])
    assert (Path(tmp_path) / Path("AAPL_MACDLine_SignalLine_MACDHistogram_2020-01-01_00-00-00.png")).exists()


def test_visualizer_can_draw_sma_plots() -> None:
    visualizer = SimpleMovingAverageVisualizer()
    assert visualizer._can_draw_indicator("SMA_200")
    assert visualizer._can_draw_indicator("SMA_50")
    assert not visualizer._can_draw_indicator("MACDLine")


@freeze_time("2020-01-01")
def test_sma_visualizer_outputs_png_image_in_the_report_output_path(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, fake_data_source: DataSource
) -> None:
    visualizer = visualizer_factory()
    monkeypatch.setattr("reporting.visualizer.APP_SETTINGS.report_output_path", tmp_path)
    data = fake_data_source.load_to_dataframe("AAPL")
    data["SMA_200"] = pd.Series([47.0, 31.0, 28.0, 37.0, 52.0], index=data.index, name="SMA_200")
    visualizer.plot(data, "AAPL", ["SMA_200"])
    assert (tmp_path / Path("AAPL_SMA_200_2020-01-01_00-00-00.png")).exists()


def test_visualizer_can_draw_ema_plots() -> None:
    visualizer = ExponentialMovingAverageVisualizer()
    assert visualizer._can_draw_indicator("EMA_200")
    assert visualizer._can_draw_indicator("EMA_50")
    assert not visualizer._can_draw_indicator("MACDLine")


@freeze_time("2020-01-01")
def test_ema_visualizer_outputs_png_image_in_the_report_output_path(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, fake_data_source: DataSource
) -> None:
    visualizer = visualizer_factory()
    monkeypatch.setattr("reporting.visualizer.APP_SETTINGS.report_output_path", tmp_path)
    data = fake_data_source.load_to_dataframe("AAPL")
    data["EMA_200"] = pd.Series([47.0, 31.0, 28.0, 37.0, 52.0], index=data.index, name="EMA_200")
    visualizer.plot(data, "AAPL", ["EMA_200"])
    assert (tmp_path / Path("AAPL_EMA_200_2020-01-01_00-00-00.png")).exists()
