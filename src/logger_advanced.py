import logging
from config import LOG_JSON, LOG_LEVEL
import json
from storage.db import init_db
from datetime import datetime

_logger = None

def get_advanced_logger(name=__name__):
    global _logger
    if _logger:
        return _logger
    import sys
    level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(level)
    handler = logging.StreamHandler(sys.stdout)
    if LOG_JSON:
        formatter = logging.Formatter('%(message)s')
    else:
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    _logger = logger
    return logger

def audit_event(event_type, payload, telegram_id=None):
    """Store audit event in DB (requires DB init)."""
    conn = init_db()
    ts = datetime.utcnow().isoformat()
    c = conn.cursor()
    c.execute("INSERT INTO alerts(telegram_id, type, payload, ts) VALUES (?,?,?,?)", (telegram_id, event_type, json.dumps(payload), ts))
    conn.commit()
    get_advanced_logger('audit').info("AUDIT %s %s %s", event_type, telegram_id, payload)
