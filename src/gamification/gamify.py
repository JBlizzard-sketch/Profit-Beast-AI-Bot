"""Gamification: leaderboards, badges, points, vault contributions."""
from ..storage.db import init_db
from ..logger_setup import get_logger
from datetime import datetime

log = get_logger(__name__)
conn = init_db()

def add_points(telegram_id, points):
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO leaderboards(telegram_id, points, badges) VALUES (?,?,?)', (telegram_id,0,''))
    c.execute('UPDATE leaderboards SET points = points + ? WHERE telegram_id = ?', (points, telegram_id))
    conn.commit()
    log.info("Added %s points to %s", points, telegram_id)

def get_leaderboard(top_n=10):
    c = conn.cursor()
    c.execute('SELECT telegram_id, points FROM leaderboards ORDER BY points DESC LIMIT ?', (top_n,))
    return c.fetchall()

def award_badge(telegram_id, badge_name):
    c = conn.cursor()
    c.execute('SELECT badges FROM leaderboards WHERE telegram_id=?', (telegram_id,))
    row = c.fetchone()
    badges = row[0] if row else ''
    badges_list = badges.split(',') if badges else []
    if badge_name not in badges_list:
        badges_list.append(badge_name)
    c.execute('INSERT OR IGNORE INTO leaderboards(telegram_id, points, badges) VALUES (?,?,?)', (telegram_id,0,','.join(badges_list)))
    c.execute('UPDATE leaderboards SET badges=? WHERE telegram_id=?', (','.join(badges_list), telegram_id))
    conn.commit()
    log.info("Awarded badge %s to %s", badge_name, telegram_id)
