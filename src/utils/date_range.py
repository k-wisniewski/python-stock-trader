from datetime import datetime, timedelta
from typing import Annotated, Self

from pydantic import BaseModel, Field, PositiveInt, model_validator, validate_call


class DateRange(BaseModel):
    start: datetime = Field(frozen=True)
    end: datetime = Field(frozen=True)

    @model_validator(mode="after")
    def validate_start_before_end(self: Self) -> Self:
        if self.start > self.end:
            raise ValueError("start datetime can't be before end datetime")
        return self

    @classmethod
    @validate_call
    def years_back(cls, years: PositiveInt) -> Self:
        now = datetime.now()
        return cls(start=now - timedelta(days=365 * years), end=now)

    @classmethod
    @validate_call
    def months_back(cls, months: PositiveInt) -> Self:
        now = datetime.now()
        return cls(start=now - timedelta(days=30 * months), end=now)

    @classmethod
    @validate_call
    def days_back(cls, days: PositiveInt) -> Self:
        now = datetime.now()
        return cls(start=now - timedelta(days=days), end=now)

    @classmethod
    @validate_call
    def hours_back(cls, hours: PositiveInt) -> Self:
        now = datetime.now()
        return cls(start=now - timedelta(hours=hours), end=now)

    @classmethod
    @validate_call
    def from_last(cls, last_str: Annotated[str, Field(pattern=r"^\d*[hdmy]$")]) -> Self:
        if "h" in last_str:
            return cls.hours_back(_get_numeric_val_from_str(last_str, "h"))
        elif "d" in last_str:
            return cls.days_back(_get_numeric_val_from_str(last_str, "d"))
        elif "m" in last_str:
            return cls.months_back(_get_numeric_val_from_str(last_str, "m"))
        return cls.years_back(_get_numeric_val_from_str(last_str, "y"))


def _get_numeric_val_from_str(last_str: str, delim: str) -> int:
    return int(last_str[: last_str.index(delim)])
