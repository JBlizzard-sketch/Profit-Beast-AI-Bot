"""Application entrypoint for AltTrade AI Bot (ProfitBeast Edition)"""
from logger_setup import get_logger
from telegram_bot import run_bot
from config import ENV_MODE
log = get_logger("app_main")

def main():
    log.info("Starting AltTrade AI Bot. Mode=%s", ENV_MODE)
    run_bot()

if __name__ == "__main__":
    main()
