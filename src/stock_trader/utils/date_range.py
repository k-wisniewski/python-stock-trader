from datetime import datetime, timedelta
from typing import Self



class DateRange:
    start: datetime
    end: datetime

    def __init__(self: Self, start: datetime, end: datetime) -> None:
        self.start = start
        self.end = end

    @classmethod
    def from_last(cls, last_str: str) -> Self:
        if "h" in last_str:
            now = datetime.now()
            return cls(start=now - timedelta(hours=_get_numeric_val_from_str(last_str, "h")), end=now)
        elif "d" in last_str:
            now = datetime.now()
            return cls(start=now - timedelta(days=_get_numeric_val_from_str(last_str, "d")), end=now)
        elif "m" in last_str:
            now = datetime.now()
            return cls(start=now - timedelta(days=30 * _get_numeric_val_from_str(last_str, "m")), end=now)
        now = datetime.now()
        return cls(start=now - timedelta(days=365 * _get_numeric_val_from_str(last_str, "y")), end=now)


def _get_numeric_val_from_str(last_str: str, delim: str) -> int:
    return int(last_str[: last_str.index(delim)])
