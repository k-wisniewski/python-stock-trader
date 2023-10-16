import datetime
from pydantic import ValidationError

import pytest
from stock_trader.utils.date_range import DateRange
from freezegun import freeze_time

FROZEN_TIME = "2023-09-12 12:00:00"


@freeze_time(FROZEN_TIME)
def test_years_back() -> None:
    date_range = DateRange.years_back(5)
    assert date_range.end == datetime.datetime.now()
    assert datetime.datetime.now() == datetime.timedelta(days=5 * 365) + date_range.start


def test_years_back_with_negative_values() -> None:
    with pytest.raises(ValidationError):
        DateRange.years_back(-5)


@freeze_time(FROZEN_TIME)
def test_months_back() -> None:
    date_range = DateRange.months_back(5)
    assert date_range.end == datetime.datetime.now()
    assert datetime.datetime.now() == datetime.timedelta(days=5 * 30) + date_range.start


def test_months_back_with_negative_values() -> None:
    with pytest.raises(ValidationError):
        DateRange.months_back(-5)


@freeze_time(FROZEN_TIME)
def test_days_back() -> None:
    date_range = DateRange.days_back(5)
    assert date_range.end == datetime.datetime.now()
    assert datetime.datetime.now() == datetime.timedelta(days=5) + date_range.start


def test_days_back_with_negative_values() -> None:
    with pytest.raises(ValidationError):
        DateRange.days_back(-5)


@freeze_time(FROZEN_TIME)
def test_hours_back() -> None:
    date_range = DateRange.hours_back(5)
    assert date_range.end == datetime.datetime.now()
    assert datetime.datetime.now() == datetime.timedelta(hours=5) + date_range.start


def test_hours_back_with_negative_values() -> None:
    with pytest.raises(ValidationError):
        DateRange.hours_back(-5)


@pytest.mark.parametrize(
    "last_str,delta",
    [
        ("5y", datetime.timedelta(days=365 * 5)),
        ("7m", datetime.timedelta(days=30 * 7)),
        ("4d", datetime.timedelta(days=4)),
        ("3h", datetime.timedelta(hours=3)),
    ],
)
def test_from_last(last_str: str, delta: datetime.timedelta) -> None:
    with freeze_time(FROZEN_TIME) as freezer:
        date_range = DateRange.from_last(last_str)
        assert date_range.end == freezer()
        assert date_range.start == freezer() - delta


def test_from_last_raises_when_invalid_specifier() -> None:
    with pytest.raises(ValidationError):
        DateRange.from_last("abra cadabra")


def test_start_always_before_end() -> None:
    with pytest.raises(ValidationError):
        now = datetime.datetime.now()
        future = now + datetime.timedelta(days=3)
        DateRange(start=future, end=now)
