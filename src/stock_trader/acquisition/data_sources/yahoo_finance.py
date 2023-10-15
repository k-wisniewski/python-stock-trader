from typing import Self, cast
import pandas as pd
import yfinance as yf
from src.stock_trader.acquisition.data_sources.data_source import DataSource, TickerNotFoundError


class YFinanceDataSource(DataSource):
    def load_to_dataframe(
        self: Self,
        ticker: str,
    ) -> pd.DataFrame:
        stock = yf.Ticker(ticker)
        df = stock.history(period="max")
        if len(df) == 0:
            raise TickerNotFoundError()
        df.index = self._convert_index(df)
        return cast(pd.DataFrame, df)

    def _convert_index(self: Self, df: pd.DataFrame) -> pd.DatetimeIndex:
        # tz_convert(None) removes the timezone information from the index
        # df has DatetimeIndex so we can use tz_convert method
        return df.index.tz_convert(None)  # type: ignore

    def __str__(self: Self) -> str:
        return "YFinance"
