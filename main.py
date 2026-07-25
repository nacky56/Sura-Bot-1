from flask import Flask, request
import requests
import json
from datetime import datetime

app = Flask(__name__)

BOT_TOKEN = "8992624703:AAG_qoSZvlBqAVdlrkGzpcm1RLBEHYpMv-o"
CHAT_ID = "1821139533"

@app.route('/')
def home():
    return "Running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        raw = request.data.decode('utf-8')
        try:
            data = json.loads(raw)
        except:
            data = {"message": raw}

        symbol  = data.get("symbol", "N/A")
        price   = data.get("price", "N/A")
        message = data.get("message", "N/A").strip()
        now     = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

        # Buy/Sell emoji colors
        msg_lower = message.lower()
        if "buy" in msg_lower or "long" in msg_lower or "bullish" in msg_lower:
            emoji = "🟢 BUY SIGNAL"
        elif "sell" in msg_lower or "short" in msg_lower or "bearish" in msg_lower:
            emoji = "🔴 SELL SIGNAL"
        else:
            emoji = "🔔 ALERT"

        text = (
            f"{emoji}\n"
            f"━━━━━━━━━━━━━━━\n"
            f"📊 Symbol: {symbol}\n"
            f"💰 Price:  {price}\n"
            f"📢 Signal: {message}\n"
            f"🕐 Time:   {now}\n"
            f"━━━━━━━━━━━━━━━"
        )

        result = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id": CHAT_ID, "text": text}
        )
        print(f"Telegram response: {result.text}")
        return "OK", 200

    except Exception as e:
        print(f"Error: {e}")
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
