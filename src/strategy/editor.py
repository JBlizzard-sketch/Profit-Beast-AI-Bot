"""Strategy editor: store JSON strategies, allow edit, list, and simple simulation."""
import json
from storage.db import init_db
from logger_setup import get_logger
from datetime import datetime

log = get_logger(__name__)
conn = init_db()

def save_strategy(telegram_id, name, strategy_json):
    c = conn.cursor()
    now = datetime.utcnow().isoformat()
    c.execute('''CREATE TABLE IF NOT EXISTS strategies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    owner_id INTEGER,
                    name TEXT,
                    strategy_json TEXT,
                    created_at TEXT
                )''')
    c.execute('INSERT INTO strategies(owner_id, name, strategy_json, created_at) VALUES (?,?,?,?)',
              (telegram_id, name, json.dumps(strategy_json), now))
    conn.commit()
    log.info("Strategy saved: %s by %s", name, telegram_id)

def list_strategies(owner_id=None):
    c = conn.cursor()
    if owner_id:
        c.execute('SELECT id, name, created_at FROM strategies WHERE owner_id=?', (owner_id,))
    else:
        c.execute('SELECT id, name, created_at FROM strategies')
    return c.fetchall()

def simulate_strategy(strategy_json, market_data):
    """Very simple rule-based simulation: strategy_json contains rules like {'symbol':'BTC/USDT','threshold':0.01,'side':'buy'}"""
    # market_data: dict with 'price_series' list
    start_price = market_data.get('price_series',[1.0])[0]
    end_price = market_data.get('price_series')[-1]
    change = (end_price - start_price)/start_price
    # naive simulation: if change > threshold and side buy -> profit
    threshold = strategy_json.get('threshold', 0.01)
    side = strategy_json.get('side','buy')
    profit = 0.0
    if side=='buy' and change > threshold:
        profit = change
    elif side=='sell' and change < -threshold:
        profit = -change
    return {'profit_pct': profit}

if __name__ == '__main__':
    # self-test
    save_strategy(1, 'mean_reversion', {'symbol':'BTC/USDT','threshold':0.02,'side':'buy'})
    print(list_strategies(1))
