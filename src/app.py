"""Simple intraday trading simulator using LLM decisions."""

from dataclasses import dataclass
from datetime import datetime, time as dtime, timezone, timedelta
import time

import schedule

from broker import Broker, RealBroker
from database import TradeDatabase
from llm_decision import LLMDecisionMaker

@dataclass
class Config:
    budget: float
    llm_provider: str
    llm_api_key: str
    broker_api_key: str | None = None
    interval: int = 60  # seconds between LLM decisions

class TradingApp:
    def __init__(self, config: Config):
        self.config = config
        self.db = TradeDatabase()
        if config.broker_api_key:
            self.broker = RealBroker(config.broker_api_key)
        else:
            self.broker = Broker()
        self.broker.set_cash(config.budget)
        self.llm = LLMDecisionMaker(config.llm_provider, config.llm_api_key)

    def trading_step(self, context: str):
        decisions = self.llm.decide(context, self.broker.cash)
        for action, symbol in decisions:
            price = self.broker.get_price(symbol)
            try:
                if action == "BUY":
                    trade = self.broker.buy(symbol, 1, price)
                    self.db.log_trade(trade)
                elif action == "SELL":
                    qty = self.broker.positions.get(symbol, 0)
                    if qty > 0:
                        trade = self.broker.sell(symbol, qty, price)
                        self.db.log_trade(trade)
                # HOLD does nothing
            except ValueError as exc:
                print(f"Could not execute {action} {symbol}: {exc}")

    def is_market_open(self) -> bool:
        tz = timezone(timedelta(hours=5, minutes=30))  # IST
        now = datetime.now(tz).time()
        return dtime(9, 15) <= now <= dtime(15, 30)

    def start(self, context: str):
        schedule.every(self.config.interval).seconds.do(self.trading_step, context)
        while True:
            if self.is_market_open():
                schedule.run_pending()
            time.sleep(1)

def main():
    import os
    provider = os.environ.get("LLM_PROVIDER", "openai")
    if provider.lower() == "gemini":
        api_key = os.environ.get("GEMINI_API_KEY", "")
    else:
        api_key = os.environ.get("OPENAI_API_KEY", "")
        provider = "openai"
    broker_key = os.environ.get("BROKER_API_KEY")
    config = Config(
        budget=10000.0,
        llm_provider=provider,
        llm_api_key=api_key,
        broker_api_key=broker_key,
    )
    app = TradingApp(config)
    context = "Historical data goes here"
    app.start(context)

if __name__ == "__main__":
    main()
