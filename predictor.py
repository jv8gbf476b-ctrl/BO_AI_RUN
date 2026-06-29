"""
BO_AI v4.1
predictor.py
予測・通知・pending保存
"""

from datetime import datetime
from zoneinfo import ZoneInfo

from config import THRESHOLD, TIMEZONE
from pending import load_pending, save_pending
from telegram_bot import send_telegram
from model import predict_signal


def make_confidence_text(confidence):
    if confidence >= 0.90:
        return "★★★★★"
    elif confidence >= 0.80:
        return "★★★★☆"
    elif confidence >= 0.70:
        return "★★★☆☆"
    elif confidence >= 0.60:
        return "★★☆☆☆"
    else:
        return "★☆☆☆☆"


def decide_signal(up_prob, down_prob):
    if up_prob >= THRESHOLD:
        return "HIGH", "📈 HIGH エントリー"

    if down_prob >= THRESHOLD:
        return "LOW", "📉 LOW エントリー"

    return "SKIP", "⚪ 見送り"


def predict_and_notify(model, data):

    result = predict_signal(model, data)

    up_prob = result["up_prob"]
    down_prob = result["down_prob"]
    confidence = result["confidence"]

    signal, signal_text = decide_signal(
        up_prob,
        down_prob
    )

    latest_time = data.index[-1]
    latest_close = float(data["Close"].iloc[-1])

    jst_time = latest_time.tz_convert(
        ZoneInfo(TIMEZONE)
    )

    now_jst = datetime.now(
        ZoneInfo(TIMEZONE)
    )

    delay_minutes = int(
        (now_jst - jst_time.to_pydatetime()).total_seconds() / 60
    )

    signal_id = jst_time.strftime("%Y%m%d_%H%M")

    pending = load_pending()

    if not pending or pending.get("id") != signal_id:

        save_pending({
            "id": signal_id,
            "entry_time": latest_time.isoformat(),
            "entry_time_jst": jst_time.isoformat(),
            "entry_close": latest_close,
            "signal": signal,
            "up_prob": round(up_prob, 6),
            "down_prob": round(down_prob, 6),
            "confidence": round(confidence, 6),
            "delay_minutes": delay_minutes,
        })

    message = f"""
🤖 BO_AI_RUN

ID: {signal_id}

足時刻: {jst_time.strftime("%Y-%m-%d %H:%M")}

通知時刻: {now_jst.strftime("%Y-%m-%d %H:%M:%S")}

遅延: {delay_minutes}分

現在価格: {latest_close:.3f}

📈 上昇確率 : {up_prob*100:.2f}%
📉 下降確率 : {down_prob*100:.2f}%

信頼度 : {make_confidence_text(confidence)}

判定 : {signal_text}
"""

    print(message)

    send_telegram(message)
