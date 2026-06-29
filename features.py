"""
BO_AI v4.1
features.py
特徴量生成
"""

import pandas as pd


def build_features(data: pd.DataFrame) -> pd.DataFrame:
    data["MA5"] = data["Close"].rolling(5).mean()
    data["MA10"] = data["Close"].rolling(10).mean()
    data["MA20"] = data["Close"].rolling(20).mean()
    data["EMA20"] = data["Close"].ewm(span=20).mean()
    data["EMA50"] = data["Close"].ewm(span=50).mean()

    data["Return"] = data["Close"].pct_change()
    data["Return3"] = data["Close"].pct_change(3)
    data["Return5"] = data["Close"].pct_change(5)

    delta = data["Close"].diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    data["RSI"] = 100 - (100 / (1 + rs))

    tr1 = data["High"] - data["Low"]
    tr2 = (data["High"] - data["Close"].shift()).abs()
    tr3 = (data["Low"] - data["Close"].shift()).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    data["ATR"] = tr.rolling(14).mean()

    data["Hour"] = data.index.hour
    data["DayOfWeek"] = data.index.dayofweek

    std20 = data["Close"].rolling(20).std()
    data["BB_Middle"] = data["MA20"]
    data["BB_Upper"] = data["MA20"] + std20 * 2
    data["BB_Lower"] = data["MA20"] - std20 * 2
    data["BB_Width"] = (data["BB_Upper"] - data["BB_Lower"]) / data["BB_Middle"]
    data["BB_Position"] = (data["Close"] - data["BB_Lower"]) / (data["BB_Upper"] - data["BB_Lower"])

    ema12 = data["Close"].ewm(span=12).mean()
    ema26 = data["Close"].ewm(span=26).mean()
    data["MACD"] = ema12 - ema26
    data["MACD_Signal"] = data["MACD"].ewm(span=9).mean()
    data["MACD_Hist"] = data["MACD"] - data["MACD_Signal"]

    data["MA5_Gap"] = (data["Close"] - data["MA5"]) / data["MA5"]
    data["MA10_Gap"] = (data["Close"] - data["MA10"]) / data["MA10"]
    data["EMA20_Gap"] = (data["Close"] - data["EMA20"]) / data["EMA20"]

    data["Momentum3"] = data["Close"] - data["Close"].shift(3)
    data["Momentum5"] = data["Close"] - data["Close"].shift(5)
    data["Momentum10"] = data["Close"] - data["Close"].shift(10)

    data["Body"] = data["Close"] - data["Open"]
    data["BodyAbs"] = data["Body"].abs()
    data["Range"] = data["High"] - data["Low"]

    data["UpperWick"] = data["High"] - data[["Open", "Close"]].max(axis=1)
    data["LowerWick"] = data[["Open", "Close"]].min(axis=1) - data["Low"]

    data["BodyRatio"] = data["BodyAbs"] / data["Range"]
    data["UpperWickRatio"] = data["UpperWick"] / data["Range"]
    data["LowerWickRatio"] = data["LowerWick"] / data["Range"]

    data["Volatility10"] = data["Return"].rolling(10).std()
    data["TrendUp"] = (data["EMA20"] > data["EMA50"]).astype(int)
    data["CloseAboveMA20"] = (data["Close"] > data["MA20"]).astype(int)

    return data
