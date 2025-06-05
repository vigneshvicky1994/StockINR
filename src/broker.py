"""Broker interfaces used by the app."""


class Broker:
    """A dummy broker interface for paper trading.

    It uses real-time prices where possible but does not place real orders.
    """

    def __init__(self):
        self.cash = 0
        self.positions = {}

    def set_cash(self, amount: float):
        self.cash = amount

    def buy(self, symbol: str, quantity: int, price: float):
        cost = quantity * price
        if cost > self.cash:
            raise ValueError("Insufficient cash to buy")
        self.cash -= cost
        self.positions[symbol] = self.positions.get(symbol, 0) + quantity
        return {
            "type": "buy",
            "symbol": symbol,
            "quantity": quantity,
            "price": price,
        }

    def sell(self, symbol: str, quantity: int, price: float):
        if self.positions.get(symbol, 0) < quantity:
            raise ValueError("Insufficient shares to sell")
        self.positions[symbol] -= quantity
        proceeds = quantity * price
        self.cash += proceeds
        return {
            "type": "sell",
            "symbol": symbol,
            "quantity": quantity,
            "price": price,
        }

    def get_price(self, symbol: str) -> float:
        """Fetch the latest market price for a symbol using yfinance."""
        try:
            import yfinance as yf

            ticker = yf.Ticker(symbol)
            info = ticker.fast_info
            return float(info.get("lastPrice") or info.get("regularMarketPrice"))
        except Exception:
            # Fall back to a dummy price if fetching fails
            return 100.0


class RealBroker(Broker):
    """Placeholder for a real broker implementation.

    In a production setup this would talk to the broker's REST API using the
    provided API key. Here we simply reuse the dummy logic while signalling
    that real trades would be executed.
    """

    def __init__(self, api_key: str):
        super().__init__()
        self.api_key = api_key

    def buy(self, symbol: str, quantity: int, price: float):
        # TODO: integrate with real broker API
        print(f"[REAL] Buying {quantity} {symbol} @ {price}")
        return super().buy(symbol, quantity, price)

    def sell(self, symbol: str, quantity: int, price: float):
        # TODO: integrate with real broker API
        print(f"[REAL] Selling {quantity} {symbol} @ {price}")
        return super().sell(symbol, quantity, price)

