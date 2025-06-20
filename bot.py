print("Bot is running...")
import os
import logging
from datetime import datetime, time
import requests
import telegram
from telegram.ext import Updater, CommandHandler, CallbackContext
import pytz
import talib
import numpy as np

# Configure logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Load env variables
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

if not TOKEN or not CHAT_ID:
    logger.error("Telegram bot token or chat ID not set in environment variables!")
    exit(1)

bot = telegram.Bot(token=TOKEN)

# Constants for trading pairs
PAIRS = ['EURUSD', 'XAUUSD', 'BTCUSD']

# Timezones
LONDON_TZ = pytz.timezone('Europe/London')
NY_TZ = pytz.timezone('America/New_York')

# Session times (24h format)
LONDON_SESSION_START = time(8, 0)   # 8:00 London time
LONDON_SESSION_END = time(17, 0)    # 17:00 London time
NY_SESSION_START = time(13, 0)      # 13:00 London time == 8:00 New York time (EST)
NY_SESSION_END = time(22, 0)        # 22:00 London time == 17:00 New York time (EST)

# Mock data fetch (replace with real market data API)
def fetch_price_data(pair, period='1h', length=50):
    # For demo, generate random data
    close_prices = np.random.uniform(low=1.10, high=1.20, size=length)
    return close_prices

def in_session():
    now_utc = datetime.utcnow().replace(tzinfo=pytz.utc)
    now_london = now_utc.astimezone(LONDON_TZ).time()

    # Check London session
    if LONDON_SESSION_START <= now_london <= LONDON_SESSION_END:
        return True

    # Check New York session
    if NY_SESSION_START <= now_london <= NY_SESSION_END:
        return True

    return False

def calculate_ema_rsi(prices):
    ema = talib.EMA(prices, timeperiod=20)[-1]
    rsi = talib.RSI(prices, timeperiod=14)[-1]
    return ema, rsi

def generate_signal():
    if not in_session():
        logger.info("Outside trading sessions. No signals generated.")
        return None

    signals = []
    for pair in PAIRS:
        prices = fetch_price_data(pair)
        ema, rsi = calculate_ema_rsi(prices)

        last_price = prices[-1]

        if last_price > ema and rsi < 70:
            signals.append({
                'pair': pair,
                'signal': 'BUY',
                'entry': last_price,
                'stop_loss': last_price * 0.995,
                'take_profit': last_price * 1.02,
                'lot_size': 0.1
            })
        elif last_price < ema and rsi > 30:
            signals.append({
                'pair': pair,
                'signal': 'SELL',
                'entry': last_price,
                'stop_loss': last_price * 1.005,
                'take_profit': last_price * 0.98,
                'lot_size': 0.1
            })

    return signals if signals else None

def send_signal(signal):
    message = (
        f"📈 {signal['pair']} Signal\n"
        f"Type: {signal['signal']}\n"
        f"Entry: {signal['entry']:.5f}\n"
        f"Stop Loss: {signal['stop_loss']:.5f}\n"
        f"Take Profit: {signal['take_profit']:.5f}\n"
        f"Lot Size: {signal['lot_size']:.2f}"
    )
    bot.send_message(chat_id=CHAT_ID, text=message)

def start(update: telegram.Update, context: CallbackContext):
    update.message.reply_text("NathanFXBot started. Use /help for commands.")

def help_command(update: telegram.Update, context: CallbackContext):
    update.message.reply_text(
        "/test - Test bot connectivity\n"
        "/summary - Get latest signal summary\n"
        "/help - Show this help message"
    )

def test(update: telegram.Update, context: CallbackContext):
    update.message.reply_text("Bot is working! 👍")

def summary(update: telegram.Update, context: CallbackContext):
    signals = generate_signal()
    if not signals:
        update.message.reply_text("No active signals at this time.")
        return

    msg = "Latest Signals:\n"
    for sig in signals:
        msg += (
            f"\n{sig['pair']} - {sig['signal']}\n"
            f"Entry: {sig['entry']:.5f}\n"
            f"SL: {sig['stop_loss']:.5f}\n"
            f"TP: {sig['take_profit']:.5f}\n"
            f"Lot: {sig['lot_size']:.2f}\n"
        )
    update.message.reply_text(msg)

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(CommandHandler('test', test))
    dispatcher.add_handler(CommandHandler('summary', summary))

    # Periodic signal sending (every 1 hour)
    import threading
    import time as t

    def signal_loop():
        while True:
            signals = generate_signal()
            if signals:
                for sig in signals:
                    send_signal(sig)
            t.sleep(3600)  # wait 1 hour

    thread = threading.Thread(target=signal_loop, daemon=True)
    thread.start()

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':

    main()
    
from telegram import Bot

# TEST: Send signal to confirm bot is running
bot = Bot(token="8162763392:AAFF97mkCT08u9-jJ0Uu5HBS4f7N-Stc_UE")
bot.send_message(chat_id="-1002085444133", text="Bot is live ✅")
