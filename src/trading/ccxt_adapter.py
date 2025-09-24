"""CCXT adapter with sandbox mock and live stub."""
import time, random
from config import ENV_MODE, LIVE_MODE, CCXT_EXCHANGE
from logger_setup import get_logger

log = get_logger(__name__)

class MockExchange:
    def __init__(self):
        self.balances = {'USDT': 10000.0}
        self.positions = {}

    def fetch_balance(self):
        return {'total': self.balances}

    def create_order(self, symbol, side, amount, price=None):
        # simulate order execution
        ts = time.time()
        executed_price = price or (random.uniform(0.95,1.05) * 1.0)
        log.info("Mock order executed %s %s %s @%s", side, symbol, amount, executed_price)
        return {'id': int(ts), 'symbol': symbol, 'side': side, 'amount': amount, 'price': executed_price, 'timestamp': ts}

class LiveExchangeStub:
    def __init__(self):
        if not LIVE_MODE:
            raise RuntimeError("LiveExchangeStub requires LIVE_MODE=true")
        # Normally initialize ccxt exchange here using keys from env
        log.info("Initialized live exchange stub for %s", CCXT_EXCHANGE)

    def fetch_balance(self):
        raise NotImplementedError("Implement CCXT exchange wrapper for live mode")

    def create_order(self, symbol, side, amount, price=None):
        raise NotImplementedError("Implement live order via CCXT")

def get_exchange():
    if ENV_MODE == "sandbox":
        return MockExchange()
    else:
        if LIVE_MODE:
            return LiveExchangeStub()
        else:
            return MockExchange()

if __name__ == "__main__":
    ex = get_exchange()
    print("Balance:", ex.fetch_balance())
    print("Test order:", ex.create_order("BTC/USDT", "buy", 0.001))
