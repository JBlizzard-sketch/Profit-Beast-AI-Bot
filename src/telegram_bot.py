from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, filters, ContextTypes
from .config import TELEGRAM_TOKEN, ADMIN_TELEGRAM_IDS, TELEGRAM_POLLING, TRIAL_DAYS, ENV_MODE
from .logger_setup import get_logger
from .storage.db import init_db
from .trading.ccxt_adapter import get_exchange
from .ml.rug_detector import predict as rug_predict
from .ml.whale_detector import predict as whale_predict
from .ml.sentiment_fusion import compute_sentiment_scores
from .llm.groq_client import explain_signal
from .gamification.gamify import get_leaderboard, add_points, award_badge
from .marketplace.market import list_items, submit_item
from .payments.providers import StripeProvider
from .strategy.editor import list_strategies, save_strategy, simulate_strategy
from .agents.manager import start_agent, stop_agent
import datetime
import json

log = get_logger(__name__)
DB_CONN = init_db()
EXCHANGE = get_exchange()

# Main menus required by spec (minimum 8)
MAIN_MENU = [
    ("Portfolio & Balances", "menu_portfolio"),
    ("Trade Execution", "menu_trade"),
    ("ML Alerts & Signals", "menu_ml"),
    ("Sentiment Dashboard", "menu_sentiment"),
    ("Gamification", "menu_gamification"),
    ("Marketplace", "menu_marketplace"),
    ("Add/Manage Accounts", "menu_accounts"),
    ("Settings & Preferences", "menu_settings"),
    ("Help & Documentation", "menu_help"),
    ("Activity History", "menu_history"),
    ("Support / Contact Admin", "menu_support"),
]

def user_is_admin(telegram_id):
    return telegram_id in ADMIN_TELEGRAM_IDS

def build_main_keyboard(user_id):
    kb = []
    for label, key in MAIN_MENU:
        kb.append([InlineKeyboardButton(label, callback_data=key)])
    if user_is_admin(user_id):
        kb.append([InlineKeyboardButton("Admin Panel", callback_data="menu_admin")])
    return InlineKeyboardMarkup(kb)

def check_trial(telegram_id):
    c = DB_CONN.cursor()
    c.execute('SELECT trial_start, is_premium FROM users WHERE telegram_id=?', (telegram_id,))
    row = c.fetchone()
    if not row:
        return False, False
    trial_start, is_premium = row
    if is_premium:
        return True, True
    try:
        start = datetime.datetime.fromisoformat(trial_start)
    except Exception:
        return False, False
    days = (datetime.datetime.utcnow() - start).days
    return days < TRIAL_DAYS, bool(is_premium)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    uid = user.id
    username = user.username or user.full_name
    c = DB_CONN.cursor()
    now = datetime.datetime.utcnow().isoformat()
    c.execute("INSERT OR IGNORE INTO users(telegram_id, username, created_at, trial_start) VALUES (?,?,?,?)",
              (uid, username, now, now))
    DB_CONN.commit()
    kb = build_main_keyboard(uid)
    await update.message.reply_text(f"Welcome {username}! AltTrade AI Bot (ProfitBeast Edition).", reply_markup=kb)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """Available commands:
/start - open main menu
/health - show basic health
/admin_users - admin only: list users
/start_agent - admin only: start agent
/stop_agent <id> - admin only: stop agent
"""
    await update.message.reply_text(help_text)

async def health_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # basic health info
    import psutil, platform
    mem = psutil.virtual_memory()
    cpu = psutil.cpu_percent(interval=0.5)
    await update.message.reply_text(f"Mode: {ENV_MODE}\nCPU: {cpu}%\nMem: {mem.percent}%")

async def callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    uid = query.from_user.id

    trial_ok, is_premium = check_trial(uid)

    if data == 'menu_portfolio':
        bal = EXCHANGE.fetch_balance()
        await query.edit_message_text(f"Portfolio / Balances:\n{json.dumps(bal, indent=2)}", reply_markup=build_main_keyboard(uid))
    elif data == 'menu_trade':
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("Mock Buy BTC 0.001", callback_data="trade_buy_btc")],
            [InlineKeyboardButton("Mock Sell BTC 0.001", callback_data="trade_sell_btc" )]
        ])
        await query.edit_message_text("Trade Execution (sandbox):", reply_markup=kb)
    elif data.startswith('trade_'):
        # sandbox order
        if 'buy' in data:
            order = EXCHANGE.create_order('BTC/USDT','buy', 0.001)
        else:
            order = EXCHANGE.create_order('BTC/USDT','sell', 0.001)
        # reward points for trades
        add_points(uid, 10)
        await query.edit_message_text(f"Order executed: {order}", reply_markup=build_main_keyboard(uid))
    elif data == 'menu_ml':
        # run ML detectors and LLM explanation
        features = [0.1, 1.2, -1.5, 10]
        rug_pred, rug_prob = rug_predict(features)
        whale_pred, whale_score = whale_predict([1.0,0.1,-0.5])
        sentiment = compute_sentiment_scores(0.2, 0.1, -0.05)
        explanation = explain_signal('combined', {'rug':(int(rug_pred), rug_prob), 'whale':(int(whale_pred), whale_score), 'sentiment':sentiment})
        text = f"Rug: {rug_pred} (p={rug_prob})\nWhale: {whale_pred} (score={whale_score})\nSentiment fused: {sentiment['fused_score']}\n\nLLM explanation:\n{explanation}"
        await query.edit_message_text(text, reply_markup=build_main_keyboard(uid))
    elif data == 'menu_sentiment':
        # sample trending list
        trends = [{'symbol':'SOL','score':0.34},{'symbol':'DOGE','score':-0.12}]
        await query.edit_message_text(f"Sentiment trends:\n{json.dumps(trends)}", reply_markup=build_main_keyboard(uid))
    elif data == 'menu_gamification':
        lb = get_leaderboard(10)
        await query.edit_message_text(f"Leaderboard:\n{lb}", reply_markup=build_main_keyboard(uid))
    elif data == 'menu_marketplace':
        items = list_items(approved_only=True)
        text = "Marketplace items:\n" + '\n'.join([str(i) for i in items]) if items else 'No items approved yet.'
        await query.edit_message_text(text, reply_markup=build_main_keyboard(uid))
    elif data == 'menu_accounts':
        await query.edit_message_text('Manage accounts: add Twitter/X accounts and keywords via /add_account (TBD)', reply_markup=build_main_keyboard(uid))
    elif data == 'menu_settings':
        await query.edit_message_text('Settings: sandbox/live toggle controlled via .env. Preferences stored in DB (TBD).', reply_markup=build_main_keyboard(uid))
    elif data == 'menu_help':
        await query.edit_message_text('Use /help for command list.', reply_markup=build_main_keyboard(uid))
    elif data == 'menu_history':
        c = DB_CONN.cursor()
        c.execute('SELECT id, side, symbol, amount, price, profit, ts FROM trades WHERE telegram_id=? ORDER BY ts DESC LIMIT 20', (uid,))
        rows = c.fetchall()
        await query.edit_message_text('Activity history:\n' + '\n'.join([str(r) for r in rows]) if rows else 'No recent activity.', reply_markup=build_main_keyboard(uid))
    elif data == 'menu_support':
        await query.edit_message_text('Support: message will be forwarded to admin via /admin_contact (TBD).', reply_markup=build_main_keyboard(uid))
    elif data == 'menu_admin':
        if user_is_admin(uid):
            kb = InlineKeyboardMarkup([[InlineKeyboardButton(label, callback_data=key)] for label,key in [
                ('View All Users','admin_view_users'),
                ('Override Trial','admin_override_trial'),
                ('Strategy Editor','admin_strategy_editor'),
                ('Agent Control','admin_agent_control'),
                ('Audit Logs','admin_audit_logs'),
                ('Force Payment Unlock','admin_force_unlock'),
                ('ML Model Training','admin_ml_train'),
                ('Payment Management','admin_payment_mgmt'),
                ('Send Broadcast Message','admin_broadcast'),
                ('Sandbox / Test Commands','admin_sandbox'),
                ('Marketplace Admin','admin_marketplace'),
                ('System Stats','admin_stats'),
            ]])
            await query.edit_message_text('Admin Panel:', reply_markup=kb)
        else:
            await query.edit_message_text('Access denied.')
    elif data == 'admin_view_users':
        if not user_is_admin(uid):
            await query.edit_message_text('Access denied.')
            return
        c = DB_CONN.cursor()
        c.execute('SELECT telegram_id, username, created_at, trial_start, is_premium FROM users')
        rows = c.fetchall()
        await query.edit_message_text('Users:\n' + '\n'.join([str(r) for r in rows])[:4000])
    else:
        await query.edit_message_text('Not implemented yet', reply_markup=build_main_keyboard(uid))

def run_bot():
    if not TELEGRAM_TOKEN:
        log.error('No TELEGRAM_BOT_TOKEN set. Exiting.')
        return
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('health', health_command))
    # Admin commands (registered in telegram_admin module too)
    from .telegram_admin import cmd_view_users, cmd_start_agent, cmd_stop_agent
    app.add_handler(CommandHandler('admin_users', cmd_view_users))
    app.add_handler(CommandHandler('start_agent', cmd_start_agent))
    app.add_handler(CommandHandler('stop_agent', cmd_stop_agent))
    app.add_handler(CallbackQueryHandler(callback_router))
    log.info('Starting Telegram bot (polling=%s)', TELEGRAM_POLLING)
    if TELEGRAM_POLLING:
        app.run_polling()
    else:
        app.run_polling()

if __name__ == '__main__':
    run_bot()
