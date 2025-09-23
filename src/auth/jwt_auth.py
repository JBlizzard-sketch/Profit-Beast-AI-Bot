import os
import jwt
import datetime
from ..logger_setup import get_logger
from ..config import ADMIN_TELEGRAM_IDS

log = get_logger(__name__)
SECRET = os.getenv('ADMIN_JWT_SECRET', os.getenv('ADMIN_API_KEY','supersecret'))

def create_admin_token(admin_id, expires_minutes=60):
    payload = {'sub': str(admin_id), 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=expires_minutes)}
    token = jwt.encode(payload, SECRET, algorithm='HS256')
    return token

def verify_admin_token(token):
    try:
        payload = jwt.decode(token, SECRET, algorithms=['HS256'])
        return int(payload.get('sub'))
    except Exception as e:
        log.warning('JWT verify failed: %s', e)
        return None

def is_admin_telegram_id(tid):
    return tid in ADMIN_TELEGRAM_IDS

if __name__ == '__main__':
    print('Admin token sample:', create_admin_token(ADMIN_TELEGRAM_IDS[0] if ADMIN_TELEGRAM_IDS else 0))
