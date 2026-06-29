"""
BO_AI v4
history.py
history.csv の管理
"""

import os
import pandas as pd
from config import HISTORY_FILE


COLUMNS = [
    "id",
    "entry_time",
    "judge_time",
    "signal",
    "actual_direction",
    "entry_close",
    "result_close",
    "price_diff",
    "up_prob",
    "down_prob",
    "confidence",
    "delay_minutes",
    "result"
]


def initialize_history():
    """history.csvが無ければ作成"""
    if not os.path.exists(HISTORY_FILE):
        pd.DataFrame(columns=COLUMNS).to_csv(HISTORY_FILE, index=False)


def append_history(row):
    """履歴を追加"""
    initialize_history()

    df = pd.DataFrame([row])

    for col in COLUMNS:
        if col not in df.columns:
            df[col] = ""

    df = df[COLUMNS]

    df.to_csv(
        HISTORY_FILE,
        mode="a",
        header=False,
        index=False
    )


def load_history():
    """履歴を読み込む"""
    initialize_history()
    return pd.read_csv(HISTORY_FILE)


def total_record():
    """総レコード数"""
    return len(load_history())
