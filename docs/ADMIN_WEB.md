# Admin Web API

Start with:
uvicorn src.web.admin_api:app --host 0.0.0.0 --port 8000

Use ADMIN_API_KEY env var to protect endpoints. Example:
GET /admin/users?api_key=yourkey
POST /admin/agent/start with JSON {owner_id: 123, symbol: 'BTC/USDT', interval: 5}
