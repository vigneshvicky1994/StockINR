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


class ZerodhaBroker(Broker):
    """Interact with Zerodha Kite for real trading."""

    def __init__(self, api_key: str, api_secret: str, access_token: str):
        super().__init__()
        try:  # pragma: no cover - optional dependency
            from kiteconnect import KiteConnect
        except ImportError as exc:  # pragma: no cover - handle missing pkg
            raise ImportError("kiteconnect package not installed") from exc

        self.kite = KiteConnect(api_key=api_key)
        self.kite.set_access_token(access_token)
        self.api_secret = api_secret

    def buy(self, symbol: str, quantity: int, price: float):
        order_id = self.kite.place_order(
            tradingsymbol=symbol,
            exchange="NSE",
            transaction_type="BUY",
            quantity=quantity,
            order_type="MARKET",
            product="MIS",
        )
        print(f"[ZERODHA] BUY order {order_id}")
        return super().buy(symbol, quantity, price)

    def sell(self, symbol: str, quantity: int, price: float):
        order_id = self.kite.place_order(
            tradingsymbol=symbol,
            exchange="NSE",
            transaction_type="SELL",
            quantity=quantity,
            order_type="MARKET",
            product="MIS",
        )
        print(f"[ZERODHA] SELL order {order_id}")
        return super().sell(symbol, quantity, price)

    def get_price(self, symbol: str) -> float:
        ltp = self.kite.ltp(f"NSE:{symbol}")
        return float(ltp[f"NSE:{symbol}"]["last_price"])  # type: ignore[index]
