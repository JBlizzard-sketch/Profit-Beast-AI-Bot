"""FastAPI admin dashboard for AltTrade. Provides admin endpoints and webhook handlers.
Admin access is protected by ADMIN_TELEGRAM_IDS and an ADMIN_API_KEY env var for web access.
""" 
import os, json
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi.responses import JSONResponse
from storage.db import init_db
from config import ADMIN_TELEGRAM_IDS
from logger_setup import get_logger\nfrom auth.jwt_auth import verify_admin_token, is_admin_telegram_id\nfrom metrics import metrics_response, TRADE_COUNTER, ALERT_COUNTER, MODEL_RETRAIN_COUNTER
from logger_advanced import audit_event
from marketplace.market import list_items, approve_item
from agents.manager import start_agent, stop_agent, AGENTS

log = get_logger(__name__)
app = FastAPI()

from fastapi import Header, Depends
from auth.jwt_auth import verify_admin_token, is_admin_telegram_id
def get_admin_from_header(authorization: str = Header(None), api_key: str = Header(None)):
    # Prefer JWT Bearer token
    if authorization and authorization.startswith('Bearer '):
        token = authorization.split(' ',1)[1]
        admin_id = verify_admin_token(token)
        if admin_id and is_admin_telegram_id(admin_id):
            return admin_id
    # Fallback to API key header
    if api_key and api_key == ADMIN_API_KEY:
        return ADMIN_TELEGRAM_IDS[0] if ADMIN_TELEGRAM_IDS else 0
    raise HTTPException(status_code=403, detail='Forbidden')
\n
from fastapi import Header

@app.post('/admin/login')
def admin_login(payload: dict = None, x_api_key: str = Header(None)):
    """Login endpoint for React admin UI. Accepts X-API-KEY header or JSON {api_key: '...'}.
    Returns a JWT token if ADMIN_API_KEY matches the provided key.
    """
    provided = x_api_key
    if not provided and payload:
        provided = payload.get('api_key')
    if not provided:
        raise HTTPException(status_code=400, detail='API key required')
    if provided != ADMIN_API_KEY:
        raise HTTPException(status_code=403, detail='Invalid API key')
    # create a JWT token for admin usage
    from auth.jwt_auth import create_admin_token
    # use first admin id if present
    admin_id = ADMIN_TELEGRAM_IDS[0] if ADMIN_TELEGRAM_IDS else 0
    token = create_admin_token(admin_id, expires_minutes=24*60)
    return {'token': token}

conn = init_db()
ADMIN_API_KEY = os.getenv('ADMIN_API_KEY', '')

def check_admin(api_key: str = None, request_token: str = None):
    # legacy function kept for compatibility
    if request_token and request_token.startswith('Bearer '):
        token = request_token.split(' ',1)[1]
        admin_id = verify_admin_token(token)
        if admin_id and is_admin_telegram_id(admin_id):
            return True
    if api_key and api_key == ADMIN_API_KEY:
        return True
    raise HTTPException(status_code=403, detail='Forbidden')
\n    # allow Bearer token from Authorization header if present\n    if request_token and request_token.startswith('Bearer '):\n        token = request_token.split(' ',1)[1]\n        admin_id = verify_admin_token(token)\n        if admin_id and is_admin_telegram_id(admin_id):\n            return True
    # allow admin via API key (for web) or via token param in headers
    if ADMIN_API_KEY and api_key == ADMIN_API_KEY:
        return True
    raise HTTPException(status_code=403, detail='Forbidden')

@app.get('/admin/users')
def get_users(api_key: str = None):
    check_admin(api_key)
    c = conn.cursor()
    c.execute('SELECT telegram_id, username, created_at, is_premium FROM users')
    rows = c.fetchall()
    return {'users': rows}

@app.post('/admin/marketplace/{item_id}/approve')
def approve_marketplace(item_id: int, api_key: str = None):
    check_admin(api_key)
    # perform approval
    approve_item('web_admin', item_id)
    audit_event('marketplace_approve', {'item_id': item_id}, telegram_id=None)
    return {'status':'approved', 'item_id': item_id}

@app.post('/admin/agent/start')
def api_start_agent(owner_id: int, symbol: str = 'BTC/USDT', interval: int = 5, api_key: str = None):
    check_admin(api_key)
    agent_id = start_agent(owner_id, symbol, interval)
    return {'agent_id': agent_id}

@app.post('/admin/agent/stop')
def api_stop_agent(agent_id: str, api_key: str = None):
    check_admin(api_key)
    ok = stop_agent(agent_id)
    return {'stopped': ok}

@app.post('/webhook/stripe')
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')
    # For now, just log and return success
    audit_event('stripe_webhook', {'headers': dict(request.headers)}, telegram_id=None)
    return JSONResponse({'received': True})

@app.post('/webhook/mpesa')
async def mpesa_webhook(request: Request):
    data = await request.json()
    audit_event('mpesa_webhook', data, telegram_id=None)
    return JSONResponse({'received': True})
\n\n@app.get('/metrics')\ndef prometheus_metrics():\n    return metrics_response()\n

# Serve React admin UI static files if present
ui_build_dir = Path(__file__).resolve().parent.parent / 'web' / 'ui' / 'build'
if ui_build_dir.exists():
    app.mount('/ui', StaticFiles(directory=str(ui_build_dir), html=True), name='admin_ui')



@app.get('/admin/strategies')
def admin_list_strategies(admin: int = Depends(get_admin_from_header)):
    c = conn.cursor()
    c.execute('SELECT id, owner_id, name, created_at FROM strategies ORDER BY created_at DESC LIMIT 100')
    rows = c.fetchall()
    if not rows:
        # mock data
        rows = [(1, admin, 'mean_reversion', '2025-09-01T00:00:00'), (2, admin, 'momentum', '2025-09-10T00:00:00')]
    return {'strategies': rows}



@app.get('/admin/agents')
def admin_list_agents(admin: int = Depends(get_admin_from_header)):
    # list running agents from AGENTS dict if available
    try:
        from agents.manager import AGENTS
        agents = [{'id': k, 'status': 'running'} for k in AGENTS.keys()]
    except Exception:
        agents = []
    if not agents:
        agents = [{'id':'agent_demo_1','status':'stopped'},{'id':'agent_demo_2','status':'running'}]
    return {'agents': agents}

@app.post('/admin/agent/start')
def admin_start_agent(owner_id: int, symbol: str = 'BTC/USDT', interval: int = 5, admin: int = Depends(get_admin_from_header)):
    aid = start_agent(owner_id, symbol, interval)
    return {'agent_id': aid}



@app.get('/admin/audit_logs')
def admin_audit_logs(limit: int = 100, admin: int = Depends(get_admin_from_header)):
    c = conn.cursor()
    c.execute('SELECT id, telegram_id, type, payload, ts FROM alerts ORDER BY ts DESC LIMIT ?', (limit,))
    rows = c.fetchall()
    if not rows:
        rows = [(1, None, 'agent_trade', '{"profit":0.01}', '2025-09-20T00:00:00')]
    return {'audit_logs': rows}



@app.get('/admin/payments')
def admin_payments(limit: int = 50, admin: int = Depends(get_admin_from_header)):
    # Mock payment records
    payments = [{'id':'pi_mock_1','status':'succeeded','amount':999},{'id':'mpesa_mock_1','status':'pending','amount':1000}]
    return {'payments': payments}



@app.post('/admin/retrain')
def admin_retrain(admin: int = Depends(get_admin_from_header)):
    from ml.pipeline import retrain_all
    meta = retrain_all()
    return {'status':'retrained','meta': meta}



@app.get('/admin/system_stats')
def admin_system_stats(admin: int = Depends(get_admin_from_header)):
    # Return mock system stats and metrics
    import psutil
    mem = psutil.virtual_memory()
    cpu = psutil.cpu_percent(interval=0.1)
    return {'mode': ENV_MODE, 'cpu_percent': cpu, 'mem_percent': mem.percent}



@app.post('/admin/broadcast')
def admin_broadcast(message: str, admin: int = Depends(get_admin_from_header)):
    # Broadcast mock: in production, this would push to all users via Telegram
    audit_event('admin_broadcast', {'message': message}, telegram_id=admin)
    return {'sent': True, 'message': message}
