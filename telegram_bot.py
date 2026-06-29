"""
BO_AI v4
telegram_bot.py
Telegram通知
"""

import os
import requests

from config import BOT_TOKEN_ENV, CHAT_ID_ENV


def send_telegram(text: str) -> bool:
    bot_token = os.environ[BOT_TOKEN_ENV]
    chat_id = os.environ[CHAT_ID_ENV]

    try:
        response = requests.post(
            f"https://api.telegram.org/bot{bot_token}/sendMessage",
            data={
                "chat_id": chat_id,
                "text": text,
            },
            timeout=20,
        )
        response.raise_for_status()
        print("✅ Telegramへ送信しました")
        return True

    except Exception as e:
        print(f"❌ Telegram送信エラー: {e}")
        return False
