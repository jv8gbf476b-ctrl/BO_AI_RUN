"""
BO_AI v4
features.py
特徴量生成
"""

import pandas as pd


def build_features(data: pd.DataFrame) -> pd.DataFrame:
    """
    AIが学習に使う特徴量を生成
    """

    # ===== 移動平均 =====
    data["MA5"] = data["Close"].rolling(5).mean()
    data["MA10"] = data["Close"].rolling(10).mean()
    data["EMA20"] = data["Close"].ewm(span=20).mean()

    # ===== リターン =====
    data["Return"] = data["Close"].pct_change()

    # ===== RSI =====
    delta = data["Close"].diff()

    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()

    rs = gain / loss

    data["RSI"] = 100 - (100 / (1 + rs))

    # ===== ATR =====
    tr1 = data["High"] - data["Low"]
    tr2 = (data["High"] - data["Close"].shift()).abs()
    tr3 = (data["Low"] - data["Close"].shift()).abs()

    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

    data["ATR"] = tr.rolling(14).mean()

    # ===== 時間 =====
    data["Hour"] = data.index.hour
    data["DayOfWeek"] = data.index.dayofweek

    # ===== ボリンジャーバンド =====
    std20 = data["Close"].rolling(20).std()

    data["BB_Middle"] = data["EMA20"]
    data["BB_Upper"] = data["EMA20"] + std20 * 2
    data["BB_Lower"] = data["EMA20"] - std20 * 2

    # ===== MA乖離率 =====
    data["MA5_Gap"] = (
        (data["Close"] - data["MA5"])
        / data["MA5"]
    )

    data["MA10_Gap"] = (
        (data["Close"] - data["MA10"])
        / data["MA10"]
    )

    # ===== Momentum =====
    data["Momentum3"] = data["Close"] - data["Close"].shift(3)
    data["Momentum5"] = data["Close"] - data["Close"].shift(5)

    # ===== ローソク足 =====
    data["Body"] = data["Close"] - data["Open"]

    data["UpperWick"] = (
        data["High"]
        - data[["Open", "Close"]].max(axis=1)
    )

    data["LowerWick"] = (
        data[["Open", "Close"]].min(axis=1)
        - data["Low"]
    )

    # ===== ボラティリティ =====
    data["Volatility10"] = (
        data["Return"]
        .rolling(10)
        .std()
    )

    return data
