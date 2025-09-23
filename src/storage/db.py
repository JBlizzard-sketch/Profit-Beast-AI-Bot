import sqlite3
from pathlib import Path
from ..config import DB_PATH
from ..logger_setup import get_logger

log = get_logger(__name__)

def init_db():
    path = Path(DB_PATH)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    c = conn.cursor()
    # users, trials, trades, alerts, leaderboards
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    telegram_id INTEGER PRIMARY KEY,
                    username TEXT,
                    created_at TEXT,
                    trial_start TEXT,
                    is_premium INTEGER DEFAULT 0
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS trades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_id INTEGER,
                    side TEXT,
                    symbol TEXT,
                    amount REAL,
                    price REAL,
                    profit REAL,
                    ts TEXT
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_id INTEGER,
                    type TEXT,
                    payload TEXT,
                    ts TEXT
                )''')
    conn.commit()
    log.info("Database initialized at %s", DB_PATH)
    return conn

if __name__ == "__main__":
    init_db()
    print("DB init self-test done")
