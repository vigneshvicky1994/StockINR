import sqlite3
from typing import Any, Dict

class TradeDatabase:
    def __init__(self, path: str = "trades.db"):
        self.conn = sqlite3.connect(path)
        self._create_tables()

    def _create_tables(self):
        cur = self.conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                type TEXT,
                symbol TEXT,
                quantity INTEGER,
                price REAL
            )
            """
        )
        self.conn.commit()

    def log_trade(self, trade: Dict[str, Any]):
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO trades(timestamp, type, symbol, quantity, price) "
            "VALUES(datetime('now'), ?, ?, ?, ?)",
            (
                trade["type"],
                trade["symbol"],
                trade["quantity"],
                trade["price"],
            ),
        )
        self.conn.commit()
