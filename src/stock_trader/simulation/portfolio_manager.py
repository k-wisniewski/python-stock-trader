from typing import Self


class PortfolioException(Exception):
    pass


class PortfolioManager:
    def __init__(self: Self):
        self._cash = 0.0
        # Dictionary to store stock ticker symbols and their respective quantities.
        self._stocks: dict[str, int] = {}

    def recapitalize(self: Self, new_capital: float) -> None:
        self._cash = new_capital

    def buy(self: Self, ticker: str, price: float, quantity: int) -> None:
        cost = price * quantity

        if cost > self._cash:
            raise PortfolioException(f"Not enough cash to buy {quantity} shares of {ticker}.")

        self._cash -= cost
        self._stocks[ticker] = self._stocks.get(ticker, 0) + quantity

    def buy_with_entire_cash(self: Self, ticker: str, price: float) -> None:
        quantity = int(self._cash // price)
        if quantity > 0:
            self.buy(ticker, price, quantity)
        else:
            raise PortfolioException(f"Not enough cash to buy {ticker}.")

    def sell(self, ticker: str, price: float, quantity: int) -> None:
        if not self.owns(ticker) or self._stocks[ticker] < quantity:
            raise PortfolioException(f"Not enough shares of {ticker} to sell.")

        self._cash += price * quantity
        self._stocks[ticker] -= quantity

        if self._stocks[ticker] == 0:
            del self._stocks[ticker]

    def sell_all(self: Self, ticker: str, price: float) -> None:
        if not self.owns(ticker):
            raise PortfolioException(f"No shares of {ticker} to sell.")
        self.sell(ticker, price, self._stocks[ticker])

    def get_value(self: Self, current_prices: dict[str, float]) -> float:
        stock_value = sum([self._stocks[ticker] * current_prices[ticker] for ticker in self._stocks])
        return self._cash + stock_value

    def summary(self: Self, current_prices: dict[str, float]) -> dict[str, float | dict[str, int]]:
        return {
            "stocks": self._stocks,
            "cash": self._cash,
            "total_value": self.get_value(current_prices),
        }

    def owns(self, ticker: str) -> bool:
        return ticker in self._stocks and self._stocks[ticker] > 0
