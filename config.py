"""
BO_AI v4
config.py
設定はこのファイルだけで管理します。
"""

BOT_TOKEN_ENV = "BOT_TOKEN"
CHAT_ID_ENV = "CHAT_ID"

THRESHOLD = 0.70
TICKER = "JPY=X"

HISTORY_FILE = "history.csv"
PENDING_FILE = "pending_signal.json"

TIMEZONE = "Asia/Tokyo"

MODEL_PARAMS = {
    "n_estimators": 100,
    "learning_rate": 0.05,
    "random_state": 42,
    "verbose": -1,
}
