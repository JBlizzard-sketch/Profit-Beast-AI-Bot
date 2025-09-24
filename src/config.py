import os
from pathlib import Path

ROOT = Path(__file__).parent.parent
ENV_MODE = os.getenv("ENV_MODE", "sandbox")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
ADMIN_TELEGRAM_IDS = [int(x.strip()) for x in os.getenv("ADMIN_TELEGRAM_IDS","").split(",") if x.strip().isdigit()]
DB_PATH = os.getenv("DB_PATH", "/opt/render/project/src/data/database.db")
CCXT_EXCHANGE = os.getenv("CCXT_EXCHANGE", "binance")
LIVE_MODE = os.getenv("LIVE_MODE", "false").lower() in ("1","true","yes")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
TRIAL_DAYS = int(os.getenv("TRIAL_DAYS", "7"))

LOG_JSON = os.getenv("LOG_JSON","false").lower() in ("1","true","yes")
LOG_LEVEL = os.getenv("LOG_LEVEL","INFO")
TELEGRAM_POLLING = os.getenv("TELEGRAM_POLLING","true").lower() in ("1","true","yes")
