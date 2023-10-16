from pathlib import Path
from typing import NewType
from datetime import datetime
from stock_trader.reporting.history import History
from stock_trader.reporting.performance_metrics import (
    calculate_annualized_return,
    calculate_sharpe_ratio,
    calculate_max_drawdown,
)
from stock_trader.settings import APP_SETTINGS

Report = NewType("Report", str)


def create_report(history: History) -> Report:
    annualized_return = calculate_annualized_return(history)
    sharpe_ratio = calculate_sharpe_ratio(history)
    max_drawdown = calculate_max_drawdown(history)

    report = f"""
    === Trading Simulation Report ===

    - Annualized Return: {annualized_return:.2%}
    - Sharpe Ratio: {sharpe_ratio:.2f}
    - Maximum Drawdown: {max_drawdown:.2%}

    ================================
    """

    return Report(report)


def save_report(report: Report, ticker: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"report_{ticker}_{timestamp}.txt"
    with open(Path(APP_SETTINGS.report_output_path) / filename, "w") as file:
        file.write(report)

    print(f"Report saved to {filename}")
