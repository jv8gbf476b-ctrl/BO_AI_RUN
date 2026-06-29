"""
BO_AI v4.1
main.py
司令塔
"""

import pandas as pd

from data import fetch_data
from features import build_features
from model import train_model
from predictor import predict_and_notify
from grading import judge_signal
from pending import load_pending


def grade_pending(data):

    pending = load_pending()

    if pending is None:
        print("前回シグナルなし")
        return

    entry_time = pd.Timestamp(
        pending["entry_time"]
    )

    future = data[
        data.index > entry_time
    ]

    if future.empty:
        print("まだ採点できません")
        return

    result_time = future.index[0]
    result_close = float(
        future.iloc[0]["Close"]
    )

    judge_signal(
        pending=pending,
        result_time=result_time,
        result_close=result_close,
    )


def main():

    print("===== BO_AI START =====")

    data = fetch_data()

    data = build_features(data)

    data = data.dropna()

    grade_pending(data)

    model = train_model(data)

    predict_and_notify(
        model=model,
        data=data,
    )

    print("===== BO_AI END =====")


if __name__ == "__main__":
    main()
