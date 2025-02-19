import requests
import telebot
import websocket
import json
import pandas as pd

TELEGRAM_BOT_TOKEN = "7634325376:AAHFqGzi6w5PnLqSd-pF_SCC1eXfuy-cjiA"
TELEGRAM_CHAT_ID = "8027632810"

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

DERIV_API_URL = "wss://ws.deriv.com/websockets/v3"

def send_signal(message):
    bot.send_message(TELEGRAM_CHAT_ID, message)

def calculate_ema(data, period):
    return data.ewm(span=period, adjust=False).mean()

def calculate_rsi(data, period=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

ws = websocket.WebSocket()
ws.connect(DERIV_API_URL)

request_data = {
    "ticks_history": "R_75",
    "count": 100,
    "end": "latest",
    "style": "candles",
    "granularity": 60,
    "subscribe": 1
}
ws.send(json.dumps(request_data))

def on_message(ws, message):
    data = json.loads(message)
    if "candles" in data:
        df = pd.DataFrame(data["candles"])
        df["ema_50"] = calculate_ema(df["close"], 50)
        df["ema_200"] = calculate_ema(df["close"], 200)
        df["rsi"] = calculate_rsi(df["close"])
        last_row = df.iloc[-1]

        if last_row["ema_50"] > last_row["ema_200"] and last_row["rsi"] < 30:
            send_signal("BUY Signal for Volatility 75! (EMA 50 > EMA 200 & RSI < 30)")
        elif last_row["ema_50"] < last_row["ema_200"] and last_row["rsi"] > 70:
            send_signal("SELL Signal for Volatility 75! (EMA 50 < EMA 200 & RSI > 70)")

ws.run_forever(on_message=on_message)
