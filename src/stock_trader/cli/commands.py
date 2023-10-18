from datetime import datetime
import click
from pathlib import Path

from stock_trader.acquisition.data_sources.data_source_factory import Source, data_source_factory
from stock_trader.acquisition.data_loaders.data_loader_factory import data_loader_factory
from stock_trader.reporting.visualizer_factory import visualizer_factory
from stock_trader.utils.date_range import DateRange
from stock_trader.workflows.backtesting import BacktestingWorkflow
from stock_trader.trading_algorithms.factory import indicator_factory, signal_factory
from stock_trader.workflows.plotting import PlottingWorkflow


@click.command()
@click.option(
    "--signal-name",
    help="signal to use for trading",
    prompt=True,
    type=click.Choice(["MovingAverageCrossover", "RSI", "MACD"], case_sensitive=False),
)
@click.option(
    "--initial-lump-sum",
    help="initial investment sum in USD",
    type=click.FLOAT,
    prompt=True,
)
@click.pass_context
def backtest(ctx: click.Context, signal_name: str, initial_lump_sum: float) -> None:
    signal = signal_factory(signal_name)
    workflow = BacktestingWorkflow(ctx.obj["tickers"], ctx.obj["data_loader"], signal)
    workflow.backtest(ctx.obj["date_range"], initial_lump_sum)

@click.command()
@click.pass_context
def demo_backtest(ctx: click.Context) -> None:
    signal = signal_factory("RSI")
    workflow = BacktestingWorkflow(ctx.obj["tickers"], ctx.obj["data_loader"], signal)
    workflow.backtest(ctx.obj["date_range"], 1000000)

@click.command()
@click.option(
    "--indicator-name",
    help="indicator to plot",
    prompt=True,
    type=click.Choice(
        ["RAW", "MACD", "RSI_14", "EMA_5", "SMA_200"],
        case_sensitive=False,
    ),
)
@click.pass_context
def plot(ctx: click.Context, indicator_name: str) -> None:
    workflow = PlottingWorkflow(
        ctx.obj["tickers"],
        ctx.obj["data_loader"],
        visualizer_factory(),
        indicator_factory,
    )
    workflow.plot(indicator_name, ctx.obj["date_range"])

@click.command()
@click.pass_context
def demo_plot(ctx: click.Context) -> None:
    workflow = PlottingWorkflow(
        ctx.obj["tickers"],
        ctx.obj["data_loader"],
        visualizer_factory(),
        indicator_factory,
    )
    workflow.plot("RSI_14", ctx.obj["date_range"])


@click.group()
@click.option(
    "--data-source",
    help="source for OHLC data",
    prompt=True,
    type=click.Choice(["local", "yfinance", "alpha_vantage"], case_sensitive=False),
)
@click.option(
    "--alpha-vantage-api-key",
    help="Alpha Vantage API key",
    envvar="ALPHA_VANTAGE_API_KEY",
    type=click.STRING,
)
@click.option(
    "--ticker-list-file",
    help="[required]: file containing ticker list in new lines that the application should be processing",
    prompt=True,
    type=click.Path(
        exists=True,
        resolve_path=True,
        file_okay=True,
        dir_okay=False,
        allow_dash=True,
        readable=True,
        path_type=Path,
    ),
)
@click.option(
    "--start",
    help="start date time in ISO-8601 format",
    default=datetime.min,
    type=click.DateTime(),
)
@click.option(
    "--end",
    help="end date time in ISO-8601 format",
    default=datetime.now(),
    type=click.DateTime(),
)
@click.option("--last", help="analyze last days/months/years back", type=click.STRING)
@click.pass_context
def cli(
    ctx: click.Context,
    data_source: str,
    alpha_vantage_api_key: str | None,
    ticker_list_file: Path,
    start: datetime,
    end: datetime,
    last: str | None,
) -> None:
    data_src = None
    date_range = DateRange(start=start, end=end) if not last else DateRange.from_last(last)
    if data_source == "alpha_vantage":
        alpha_vantage_api_key = alpha_vantage_api_key or str(click.prompt("Alpha Vantage API key"))
        data_src = data_source_factory(
            Source.ALPHA_VANTAGE,
            alpha_vantage_api_key=alpha_vantage_api_key,
        )
    elif data_source == "local":
        data_src = data_source_factory(Source.LOCAL)
    else:
        data_src = data_source_factory(Source.YFINANCE)

    data_loader = data_loader_factory(data_src)
    ctx.ensure_object(dict)
    with open(ticker_list_file) as tickers_file:
        tickers = tickers_file.readlines()
        ctx.obj["tickers"] = [ticker.strip() for ticker in tickers]
        ctx.obj["date_range"] = date_range
        ctx.obj["data_loader"] = data_loader


cli.add_command(backtest)
cli.add_command(plot)
cli.add_command(demo_backtest)
cli.add_command(demo_plot)