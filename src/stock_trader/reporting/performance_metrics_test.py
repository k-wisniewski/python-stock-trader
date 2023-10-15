import numpy as np
import pytest
from stock_trader.reporting.history import History, HistoryItem
from stock_trader.reporting.performance_metrics import (
    calculate_annualized_return,
    calculate_max_drawdown,
    calculate_sharpe_ratio,
)


@pytest.fixture
def empty_history() -> History:
    return History([])


@pytest.fixture
def history_with_one_entry() -> History:
    return History([HistoryItem("2022-01-01", 100)])


@pytest.fixture
def history_with_multiple_entries() -> History:
    return History(
        [
            HistoryItem("2022-01-01", 100.0),
            HistoryItem("2022-01-02", 110.0),
            HistoryItem("2022-01-03", 120.0),
            HistoryItem("2022-01-04", 130.0),
            HistoryItem("2022-01-05", 140.0),
        ]
    )


def test_one_record(history_with_one_entry: History) -> None:
    assert calculate_annualized_return(history_with_one_entry) == 0.0


def test_calculate_annualized_return_with_multiple_records(
    history_with_multiple_entries: History,
) -> None:
    assert calculate_annualized_return(history_with_multiple_entries) > 0.0


def test_calculate_annualized_return_with_start_value_zero(
    history_with_multiple_entries: History,
) -> None:
    history_with_multiple_entries[0] = HistoryItem("2022-01-01", 0)
    assert calculate_annualized_return(history_with_multiple_entries) == 0.0


def test_calculate_annualized_return_with_end_value_zero(
    history_with_multiple_entries: History,
) -> None:
    history_with_multiple_entries[-1] = HistoryItem("2022-01-05", 0)
    assert calculate_annualized_return(history_with_multiple_entries) == -1.0


def test_calculate_annualized_return_with_start_and_end_values_same() -> None:
    history = [
        HistoryItem("2022-01-01", 100),
        HistoryItem("2022-01-02", 100),
        HistoryItem("2022-01-03", 100),
        HistoryItem("2022-01-04", 100),
        HistoryItem("2022-01-05", 100),
    ]
    assert calculate_annualized_return(history) == 0.0


def test_calculate_annualized_return_with_less_than_252_records() -> None:
    history = [HistoryItem(f"2022-01-{i+1}", 100) for i in range(200)]
    assert calculate_annualized_return(history) == 0.0


def test_calculate_annualized_return_with_252_records() -> None:
    history = [HistoryItem(f"2022-01-{i+1}", 100) for i in range(252)]
    assert calculate_annualized_return(history) == 0.0


def test_calculate_annualized_return_with_more_than_252_records() -> None:
    history = [HistoryItem(f"2022-01-{i+1}", 100) for i in range(300)]
    assert calculate_annualized_return(history) == 0.0


def test_calculate_annualized_return_with_empty_history(empty_history: History) -> None:
    assert calculate_annualized_return(empty_history) == 0.0


def test_calculate_annualized_return_with_one_entry_history(
    history_with_one_entry: History,
) -> None:
    assert calculate_annualized_return(history_with_one_entry) == 0.0


def test_calculate_sharpe_ratio_with_empty_history(empty_history):
    assert np.isnan(calculate_sharpe_ratio(empty_history))


def test_calculate_sharpe_ratio_with_one_entry_history(history_with_one_entry):
    assert calculate_sharpe_ratio(history_with_one_entry) == float("inf")


def test_calculate_sharpe_ratio_with_multiple_entries_history(
    history_with_multiple_entries,
):
    assert calculate_sharpe_ratio(history_with_multiple_entries) == pytest.approx(8.483, rel=1e-3)


def test_calculate_max_drawdown_with_empty_history(empty_history):
    assert calculate_max_drawdown(empty_history) == 0.0


def test_calculate_max_drawdown_with_one_entry_history(history_with_one_entry):
    assert calculate_max_drawdown(history_with_one_entry) == 0.0


def test_calculate_max_drawdown_with_multiple_entries_history(
    history_with_multiple_entries,
):
    assert calculate_max_drawdown(history_with_multiple_entries) == 0.0
