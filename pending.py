"""
BO_AI v4
pending.py
pending_signal.json の管理
"""

import json
import os
from config import PENDING_FILE


def load_pending():
    """現在のPendingデータを取得"""
    if os.path.exists(PENDING_FILE):
        with open(PENDING_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def save_pending(data):
    """Pendingデータを保存"""
    with open(PENDING_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def clear_pending():
    """Pendingデータを削除"""
    if os.path.exists(PENDING_FILE):
        os.remove(PENDING_FILE)
