from dataclasses import dataclass


@dataclass
class HistoryItem:
    date: str
    value: float


History = list[HistoryItem]
