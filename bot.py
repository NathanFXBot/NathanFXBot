import os
import pandas as pd
import pandas_ta as ta
import numpy as np
from telegram import Bot
from telegram.error import TelegramError
import requests

# Your Telegram bot token and chat ID
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

bot = Bot(token=TELEGRAM_TOKEN)

def fetch_candle_data():
    # Example: fetch last 100 candles from some API (replace with your data source)
    url = 'https://api.example.com/marketdata/candles?symbol=EURUSD&interval=1h&limit=100'
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data)
    # Ensure columns: ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    return df

def generate_signals(df):
    # Calculate EMA indicators with pandas-ta
    df['ema_9'] = ta.ema(df['close'], length=9)
    df['ema_21'] = ta.ema(df['close'], length=21)

    # Example signal logic: buy when EMA9 crosses above EMA21, sell when EMA9 crosses below EMA21
    df['signal'] = 0
    df.loc[(df['ema_9'] > df['ema_21']) & (df['ema_9'].shift(1) <= df['ema_21'].shift(1)), 'signal'] = 1  # Buy
    df.loc[(df['ema_9'] < df['ema_21']) & (df['ema_9'].shift(1) >= df['ema_21'].shift(1)), 'signal'] = -1 # Sell
    return df

def send_signal(signal):
    message = ''
    if signal == 1:
        message = "Buy signal generated!"
    elif signal == -1:
        message = "Sell signal generated!"
    else:
        return

    try:
        bot.send_message(chat_id=CHAT_ID, text=message)
        print(f"Sent message: {message}")
    except TelegramError as e:
        print(f"Failed to send Telegram message: {e}")

def main():
    df = fetch_candle_data()
    df = generate_signals(df)
    last_signal = df['signal'].iloc[-1]
    send_signal(last_signal)

if __name__ == '__main__':
    main()
