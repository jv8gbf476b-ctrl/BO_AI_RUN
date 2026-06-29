"""
BO_AI v4
model.py
AI学習・予測
"""

from lightgbm import LGBMClassifier
from sklearn.model_selection import train_test_split

# AIが使う特徴量
FEATURES = [
    "Open",
    "High",
    "Low",
    "Close",
    "MA5",
    "MA10",
    "EMA20",
    "Return",
    "RSI",
    "ATR",
    "Hour",
    "DayOfWeek",
    "BB_Middle",
    "BB_Upper",
    "BB_Lower",
    "MA5_Gap",
    "MA10_Gap",
    "Momentum3",
    "Momentum5",
    "Body",
    "UpperWick",
    "LowerWick",
    "Volatility10",
]


def train_model(data):
    """
    モデル学習
    """

    X = data[FEATURES]
    y = data["Target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        shuffle=False
    )

    model = LGBMClassifier(
        n_estimators=100,
        learning_rate=0.05,
        random_state=42,
        verbose=-1
    )

    model.fit(X_train, y_train)

    return model


def predict_signal(model, data):
    """
    最新足を予測
    """

    latest = data.iloc[[-1]][FEATURES]

    prob = model.predict_proba(latest)[0]

    return {
        "down_prob": float(prob[0]),
        "up_prob": float(prob[1]),
    }
