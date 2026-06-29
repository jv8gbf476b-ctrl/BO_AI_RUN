"""
BO_AI v4
data.py
データ取得
"""

import yfinance as yf
import pandas as pd

from config import TICKER


def fetch_data():

    data = yf.download(
        TICKER,
        period="180d",
        interval="1h",
        auto_adjust=False,
        progress=False
    )

    if data.empty:
        raise RuntimeError("データ取得失敗")

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    data = data[
        ["Open", "High", "Low", "Close"]
    ].dropna()

    return data
