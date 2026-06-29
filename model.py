"""
BO_AI v4.1
model.py
AI学習・予測
"""

from lightgbm import LGBMClassifier
from sklearn.model_selection import train_test_split

FEATURES = [
    "Open",
    "High",
    "Low",
    "Close",

    "MA5",
    "MA10",
    "MA20",
    "EMA20",
    "EMA50",

    "Return",
    "Return3",
    "Return5",

    "RSI",
    "ATR",

    "Hour",
    "DayOfWeek",

    "BB_Middle",
    "BB_Upper",
    "BB_Lower",
    "BB_Width",
    "BB_Position",

    "MACD",
    "MACD_Signal",
    "MACD_Hist",

    "MA5_Gap",
    "MA10_Gap",
    "EMA20_Gap",

    "Momentum3",
    "Momentum5",
    "Momentum10",

    "Body",
    "BodyAbs",
    "Range",

    "UpperWick",
    "LowerWick",

    "BodyRatio",
    "UpperWickRatio",
    "LowerWickRatio",

    "Volatility10",

    "TrendUp",
    "CloseAboveMA20",
]


def prepare_dataset(data):
    """
    学習データを準備
    """

    data["Target"] = (
        data["Close"].shift(-1) > data["Close"]
    ).astype(int)

    data = data.dropna()

    X = data[FEATURES]
    y = data["Target"]

    return X, y, data


def train_model(data):
    """
    AI学習
    """

    X, y, _ = prepare_dataset(data)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        shuffle=False,
    )

    model = LGBMClassifier(
        n_estimators=200,
        learning_rate=0.03,
        num_leaves=31,
        max_depth=-1,
        random_state=42,
        verbose=-1,
    )

    model.fit(X_train, y_train)

    return model


def predict_signal(model, data):
    """
    最新足を予測
    """

    latest = data.iloc[[-1]][FEATURES]

    down_prob, up_prob = model.predict_proba(latest)[0]

    confidence = max(up_prob, down_prob)

    return {
        "up_prob": float(up_prob),
        "down_prob": float(down_prob),
        "confidence": float(confidence),
    }
