"""Marketplace: submit strategies, view, admin approve/reject."""
from ..storage.db import init_db
from logger_setup import get_logger
from datetime import datetime

log = get_logger(__name__)
conn = init_db()

def submit_item(submitter_id, title, description, price_cents=0):
    c = conn.cursor()
    now = datetime.utcnow().isoformat()
    c.execute('INSERT INTO marketplace(submitter_id, title, description, price_cents, approved, created_at) VALUES (?,?,?,?,?,?)',
              (submitter_id, title, description, price_cents, 0, now))
    conn.commit()
    log.info("Marketplace item submitted: %s by %s", title, submitter_id)

def list_items(approved_only=True):
    c = conn.cursor()
    if approved_only:
        c.execute('SELECT id, title, description, price_cents, created_at FROM marketplace WHERE approved=1')
    else:
        c.execute('SELECT id, title, description, price_cents, approved, created_at FROM marketplace')
    return c.fetchall()

def approve_item(admin_id, item_id):
    c = conn.cursor()
    c.execute('UPDATE marketplace SET approved=1 WHERE id=?', (item_id,))
    conn.commit()
    log.info("Admin %s approved marketplace item %s", admin_id, item_id)
