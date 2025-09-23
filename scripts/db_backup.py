"""Simple SQLite backup script: copies DB to backups/ with timestamp; intended for cron or CI runs.""" 
import shutil, os
from pathlib import Path
from datetime import datetime
from ..src.config import DB_PATH
from ..src.logger_setup import get_logger

log = get_logger(__name__)
BACKUP_DIR = Path(os.getenv('DB_BACKUP_DIR','/mnt/data/alttrade_backups'))
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

def backup_db():
    src = Path(DB_PATH)
    if not src.exists():
        log.error('DB file not found: %s', DB_PATH)
        return None
    ts = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    dest = BACKUP_DIR / f'alttrade_db_{ts}.sqlite'
    shutil.copy2(src, dest)
    log.info('DB backed up to %s', dest)
    return dest

if __name__ == '__main__':
    print('Backing up DB...')
    print(backup_db())
