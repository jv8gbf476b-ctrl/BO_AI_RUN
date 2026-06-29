"""
BO_AI v4.7
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
    "RSI_Slope",

    "ATR",
    "ATR_Ratio",

    "PLUS_DI",
    "MINUS_DI",
    "ADX",
    "ADX_Slope",

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
    "MACD_Slope",

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
    "EMA_Cross",
    "CloseAboveMA20",

    "High20",
    "Low20",
    "DonchianWidth",

    "Stoch_K",
    "Stoch_D",

    "ROC10",
]


def prepare_dataset(data):

    data["Target"] = (
        data["Close"].shift(-1) > data["Close"]
    ).astype(int)

    data = data.dropna()

    X = data[FEATURES]
    y = data["Target"]

    return X, y, data


def train_model(data):

    X, y, _ = prepare_dataset(data)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        shuffle=False,
    )

    model = LGBMClassifier(
        n_estimators=500,
        learning_rate=0.02,
        num_leaves=63,
        max_depth=-1,
        min_child_samples=15,
        subsample=0.9,
        colsample_bytree=0.9,
        reg_alpha=0.1,
        reg_lambda=0.1,
        random_state=42,
        verbose=-1,
    )

    model.fit(X_train, y_train)

    return model


def get_feature_importance(model):

    importance = sorted(
        zip(
            FEATURES,
            model.feature_importances_,
        ),
        key=lambda x: x[1],
        reverse=True,
    )

    return importance


def predict_signal(model, data):

    latest = data.iloc[[-1]][FEATURES]

    down_prob, up_prob = model.predict_proba(latest)[0]

    confidence = max(
        up_prob,
        down_prob,
    )

    importance = get_feature_importance(model)[:5]

    return {
        "up_prob": float(up_prob),
        "down_prob": float(down_prob),
        "confidence": float(confidence),
        "importance": importance,
    }
