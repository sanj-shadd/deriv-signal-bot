import requests
import telebot
import websocket
import json

TELEGRAM_BOT_TOKEN = "7634325376:AAHFqGzi6w5PnLqSd-pF_SCC1eXfuy-cjiA"
TELEGRAM_CHAT_ID = "8027632810"

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

DERIV_API_URL = "wss://ws.deriv.com/websockets/v3"

def send_signal(message):
    bot.send_message(TELEGRAM_CHAT_ID, message)

def calculate_ema(prices, period):
    ema = []
    multiplier = 2 / (period + 1)
    ema.append(prices[0])  # First EMA is just the first price
    for price in prices[1:]:
        ema.append((price - ema[-1]) * multiplier + ema[-1])
    return ema

def calculate_rsi(prices, period=14):
    gains, losses = [], []
    
    for i in range(1, len(prices)):
        diff = prices[i] - prices[i - 1]
        gains.append(max(diff, 0))
        losses.append(abs(min(diff, 0)))

    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    rs = avg_gain / avg_loss if avg_loss != 0 else 0
    rsi = 100 - (100 / (1 + rs))
    
    return rsi

ws = websocket.WebSocket()
ws.connect(www.deriv.com)

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
        closes = [candle["close"] for candle in data["candles"]]
        
        ema_50 = calculate_ema(closes, 50)[-1]
        ema_200 = calculate_ema(closes, 200)[-1]
        rsi = calculate_rsi(closes)

        if ema_50 > ema_200 and rsi < 30:
            send_signal("BUY Signal for Volatility 75! (EMA 50 > EMA 200 & RSI < 30)")
        elif ema_50 < ema_200 and rsi > 70:
            send_signal("SELL Signal for Volatility 75! (EMA 50 < EMA 200 & RSI > 70)")

ws.run_forever(on_message=on_message)
