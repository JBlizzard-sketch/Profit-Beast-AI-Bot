"""Live CCXT wrapper. Reads CCXT_EXCHANGE, CCXT_API_KEY, CCXT_API_SECRET from env.
Provides fetch_balance and create_order with safety checks (only if LIVE_MODE==True).
"""
import os, ccxt, logging
from config import LIVE_MODE, CCXT_EXCHANGE
from logger_setup import get_logger

log = get_logger(__name__)

def get_live_exchange():
    if not LIVE_MODE:
        raise RuntimeError('LIVE_MODE is not enabled. Set LIVE_MODE=true in .env to enable live trading.')
    api_key = os.getenv('CCXT_API_KEY') or os.getenv('EXCHANGE_API_KEY')
    api_secret = os.getenv('CCXT_API_SECRET') or os.getenv('EXCHANGE_API_SECRET')
    if not api_key or not api_secret:
        raise RuntimeError('CCXT API keys not found in environment.')
    exchange_id = CCXT_EXCHANGE
    try:
        ex_class = getattr(ccxt, exchange_id)
    except Exception as e:
        # try lowercase
        ex_class = getattr(ccxt, exchange_id.lower())
    exchange = ex_class({
        'apiKey': api_key,
        'secret': api_secret,
        'enableRateLimit': True,
    })
    log.info('Initialized CCXT exchange: %s', exchange_id)
    return exchange

class LiveExchange:
    def __init__(self):
        self.exchange = get_live_exchange()
    def fetch_balance(self):
        return self.exchange.fetch_balance()
    def create_order(self, symbol, side, amount, price=None, order_type='limit'):
        if not LIVE_MODE:
            raise RuntimeError('Live orders disabled.')
        if order_type == 'market':
            order = self.exchange.create_market_order(symbol, side, amount)
        else:
            order = self.exchange.create_limit_order(symbol, side, amount, price)
        log.info('Placed live order: %s', order)
        return order

if __name__ == '__main__':
    try:
        ex = LiveExchange()
        print(ex.fetch_balance())
    except Exception as e:
        print('Live CCXT initialization error:', e)
