"""Agents manager: run/stop simple autonomous agents (simulated)."""
import threading, time, uuid
from logger_setup import get_logger
from ..trading.ccxt_adapter import get_exchange
from ..storage.db import init_db
from logger_advanced import audit_event

log = get_logger(__name__)
conn = init_db()
AGENTS = {}

class SimpleArbitrageAgent(threading.Thread):
    def __init__(self, owner_id, symbol='BTC/USDT', interval=5):
        super().__init__()
        self.owner_id = owner_id
        self.symbol = symbol
        self.interval = interval
        self._stop = threading.Event()
        self.id = str(uuid.uuid4())
        self.exchange = get_exchange()
    def run(self):
        audit_event('agent_start', {'agent_id':self.id, 'symbol':self.symbol}, telegram_id=self.owner_id)
        while not self._stop.is_set():
            # simulate checking two markets and finding price diff
            bal = self.exchange.fetch_balance()
            # simulate a dummy opportunity occasionally
            import random
            if random.random() < 0.1:
                # pretend we executed a profitable trade
                profit = random.uniform(0.001, 0.02)
                c = conn.cursor()
                now = __import__('datetime').datetime.utcnow().isoformat()
                c.execute('INSERT INTO trades(telegram_id, side, symbol, amount, price, profit, ts) VALUES (?,?,?,?,?,?,?)',
                          (self.owner_id, 'arb', self.symbol, 0.001, 10000, profit, now))
                conn.commit()
                audit_event('agent_trade', {'agent_id':self.id, 'profit':profit}, telegram_id=self.owner_id)
                log.info("Agent %s executed arb profit %s", self.id, profit)
            time.sleep(self.interval)
        audit_event('agent_stop', {'agent_id':self.id}, telegram_id=self.owner_id)

    def stop(self):
        self._stop.set()

def start_agent(owner_id, symbol='BTC/USDT', interval=5):
    agent = SimpleArbitrageAgent(owner_id, symbol, interval)
    agent.start()
    AGENTS[agent.id] = agent
    return agent.id

def stop_agent(agent_id):
    agent = AGENTS.get(agent_id)
    if agent:
        agent.stop()
        return True
    return False

if __name__ == '__main__':
    aid = start_agent(123456, 'BTC/USDT', interval=1)
    import time
    time.sleep(3)
    stop_agent(aid)
    print('agent demo done')
