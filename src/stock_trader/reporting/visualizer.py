from typing import Self
import pandas as pd

class Visualizer:

    def plot(self: Self, data: pd.DataFrame, ticker: str, indicator_names: list[str]) -> None:
        ...
  