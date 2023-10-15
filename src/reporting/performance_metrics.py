import typing
import numpy as np

from reporting.history import History


def calculate_annualized_return(history: History) -> float:
    if len(history) < 2:
        return 0.0
    start_value = history[0].value
    end_value = history[-1].value
    if start_value == 0.0:
        return 0.0
    years = len(history) / 252  # Assuming 252 trading days in a year
    # typeshed declares type returned for operator ** as Any because of specialized version
    # that squares a number which returns an int, while the general version returns a float
    return typing.cast(float, ((end_value / start_value) ** (1.0 / years)) - 1.0)


def calculate_sharpe_ratio(history: History, risk_free_rate: float = 0.03) -> float:
    returns = [entry.value for entry in history]
    excess_returns = np.array(returns) - risk_free_rate
    return typing.cast(float, (np.mean(excess_returns) / np.std(excess_returns)))


def calculate_max_drawdown(history: History) -> float:
    if len(history) < 2:
        return 0.0
    values = [entry.value for entry in history]
    peaks = np.maximum.accumulate(values)
    drawdowns = (values - peaks) / peaks
    return typing.cast(float, (np.min(drawdowns)))
