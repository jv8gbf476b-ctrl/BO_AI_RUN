import os
import requests
import yfinance as yf
import pandas as pd
from lightgbm import LGBMClassifier
from sklearn.model_selection import train_test_split

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

ticker = "JPY=X"
data = yf.download(ticker, period="180d", interval="1h", auto_adjust=False)

if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

data = data[["Open", "High", "Low", "Close"]].dropna()

data["MA5"] = data["Close"].rolling(5).mean()
data["MA10"] = data["Close"].rolling(10).mean()
data["EMA20"] = data["Close"].ewm(span=20).mean()
data["Return"] = data["Close"].pct_change()

delta = data["Close"].diff()
gain = delta.where(delta > 0, 0).rolling(14).mean()
loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
rs = gain / loss
data["RSI"] = 100 - (100 / (1 + rs))

data["Hour"] = data.index.hour
data["DayOfWeek"] = data.index.dayofweek

tr1 = data["High"] - data["Low"]
tr2 = (data["High"] - data["Close"].shift()).abs()
tr3 = (data["Low"] - data["Close"].shift()).abs()
tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
data["ATR"] = tr.rolling(14).mean()

data["Target"] = (data["Close"].shift(-1) > data["Close"]).astype(int)
data = data.dropna()

features = [
    "Open", "High", "Low", "Close",
    "MA5", "MA10", "EMA20",
    "Return", "RSI", "Hour", "DayOfWeek", "ATR"
]

X = data[features]
y = data["Target"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, shuffle=False
)

model = LGBMClassifier(
    n_estimators=100,
    learning_rate=0.05,
    random_state=42,
    verbose=-1
)

model.fit(X_train, y_train)

latest = data.iloc[[-1]][features]
prob = model.predict_proba(latest)[0]

down_prob = prob[0]
up_prob = prob[1]

if down_prob >= 0.70:
    signal = "📉 LOW エントリー"
elif up_prob >= 0.70:
    signal = "📈 HIGH エントリー"
else:
    signal = "⚪ 見送り"

signal_id = data.index[-1].strftime("%Y%m%d_%H%M")

confidence = max(up_prob, down_prob)

if confidence >= 0.85:
    confidence_text = "★★★★★"
elif confidence >= 0.80:
    confidence_text = "★★★★☆"
elif confidence >= 0.75:
    confidence_text = "★★★☆☆"
elif confidence >= 0.70:
    confidence_text = "★★☆☆☆"
else:
    confidence_text = "★☆☆☆☆"

message = f"""
🤖 BO_AI_RUN

ID: {signal_id}

現在時刻: {data.index[-1]}
現在価格: {data['Close'].iloc[-1]:.3f}

📈 上昇確率: {up_prob*100:.2f}%
📉 下降確率: {down_prob*100:.2f}%

信頼度: {confidence_text}

判定: {signal}
"""




print(message)

if up_prob >= 0.70 or down_prob >= 0.70:
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": message
        }
    )
    print("✅ Telegramへ送信しました")
else:
    print("⚪ 見送りなので通知しません")
