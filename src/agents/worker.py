"""RQ worker entrypoint for agents. Run this in a container to process agent jobs."""
from rq import Worker, Queue, Connection
from redis import Redis
import os

listen = ['agents']
redis_url = os.getenv('REDIS_URL', 'redis://redis:6379/0')
conn = Redis.from_url(redis_url)
if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()
