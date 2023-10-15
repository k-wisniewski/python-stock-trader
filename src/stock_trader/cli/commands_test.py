from pathlib import Path
from click.testing import CliRunner
import pytest

from src.stock_trader.cli.commands import cli


@pytest.fixture(scope="function")
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture(scope="session")
def tickers_path() -> Path:
    return Path(__file__).parent / Path("test_data/test_tickers.txt")


@pytest.fixture(scope="session")
def data_path() -> Path:
    return Path(__file__).parent / Path("test_data/")


def test_help_displayed_when_usage_invalid(runner: CliRunner) -> None:
    result = runner.invoke(cli, [])
    assert result.exit_code == 0
    assert "Usage: " in result.output


def test_date_range_can_be_set_with_options_start_and_end(runner: CliRunner, tickers_path: Path) -> None:
    result = runner.invoke(
        cli,
        [
            "--data-source=yfinance",
            f"--ticker-list-file={tickers_path}",
            "--start=2023-09-13 15:16:00",
            "--end=2023-09-18 15:16:00",
            "plot",
            "--indicator-name=raw",
        ],
    )
    assert result.exit_code == 0


def test_date_range_can_be_set_with_last_option(runner: CliRunner, tickers_path: Path) -> None:
    result = runner.invoke(
        cli,
        [
            "--data-source=yfinance",
            f"--ticker-list-file={tickers_path}",
            "--last=5y",
            "plot",
            "--indicator-name=raw",
        ],
    )
    assert result.exit_code == 0


def test_when_alpha_vantage_specified_api_key_required(runner: CliRunner, tickers_path: Path) -> None:
    result = runner.invoke(
        cli,
        [
            "--data-source=alpha_vantage",
            f"--ticker-list-file={tickers_path}",
            "plot",
            "--indicator-name=raw",
        ],
        input="\nXYZ\n",
    )
    # first \n should cause the application to prompt for alpha_vantage_key once again
    assert "Alpha Vantage API key: \nAlpha Vantage API key:" in result.output
    assert result.exit_code == 0


def test_conditionally_options_are_not_required_when_conditions_not_met(runner: CliRunner, tickers_path: Path) -> None:
    # not passing alpha vantage or local should not cause the prompt to provide data folder or api key
    result = runner.invoke(
        cli,
        [
            "--data-source=yfinance",
            f"--ticker-list-file={tickers_path}",
            "plot",
            "--indicator-name=raw",
        ],
    )
    assert result.exit_code == 0


def test_ticker_list_file_required(runner: CliRunner, tickers_path: Path) -> None:
    result = runner.invoke(
        cli,
        ["--data-source=yfinance", "plot", "--indicator-name=raw"],
        input=f"\n{tickers_path}\n",
    )
    assert "Ticker list file" in result.output
    assert result.exit_code == 0
