"""Binance Pay live integration scaffold. Requires BINANCE_PAY_KEY and other credentials.
Placeholder implementation; implement SDK calls per Binance Pay docs.""" 
import os
from ..logger_setup import get_logger
log = get_logger(__name__)

def create_order(amount_cents, currency='USDT', metadata=None):
    log.info('Binance Pay create_order placeholder - implement with BINANCE_PAY_KEY')
    return {'status':'created','id':'binance_live_mock'}
