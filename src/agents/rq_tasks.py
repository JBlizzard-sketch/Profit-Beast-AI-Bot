"""RQ tasks for agents. Use RQ to enqueue agent work instead of threads for production."""
import os, time
from rq import Queue
from redis import Redis
from manager import SimpleArbitrageAgent
from logger_setup import get_logger

log = get_logger(__name__)
redis_url = os.getenv('REDIS_URL', 'redis://redis:6379/0')
redis_conn = Redis.from_url(redis_url)
q = Queue('agents', connection=redis_conn)

def enqueue_agent(owner_id, symbol='BTC/USDT', interval=5):
    # In practice, you'd enqueue a long-running worker job or schedule periodic tasks.
    # Here we enqueue a short-lived simulation job.
    job = q.enqueue(run_agent_once, owner_id, symbol)
    log.info('Enqueued agent job %s', job.id)
    return job.id

def run_agent_once(owner_id, symbol):
    # simulate a single agent action
    agent = SimpleArbitrageAgent(owner_id, symbol, interval=1)
    # run one loop iteration
    import random
    if random.random() < 0.2:
        profit = random.uniform(0.001, 0.02)
        return {'profit': profit}
    return {'profit': 0.0}
