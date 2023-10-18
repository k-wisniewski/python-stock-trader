from abc import ABC, abstractmethod
from typing import Self

import pandas as pd



class VisualizerRunner(ABC):
    
    @abstractmethod
    def plot(self: Self, data: dict[str, pd.DataFrame], tickers: list[str], indicator_names: list[str]) -> None:
        ...
