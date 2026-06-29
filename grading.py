"""
BO_AI v4
grading.py
採点ロジック
"""

from zoneinfo import ZoneInfo

from history import append_history
from report import make_report_text
from telegram_bot import send_telegram
from pending import clear_pending


def judge_signal(pending, result_time, result_close):

    entry_close = float(pending["entry_close"])
    signal = pending["signal"]

    if result_close > entry_close:
        actual_direction = "HIGH"
    elif result_close < entry_close:
        actual_direction = "LOW"
    else:
        actual_direction = "FLAT"

    if signal == "HIGH":
        win = actual_direction == "HIGH"
        reason = "予測HIGHと実際HIGHが一致"

    elif signal == "LOW":
        win = actual_direction == "LOW"
        reason = "予測LOWと実際LOWが一致"

    else:
        win = actual_direction == "FLAT"

        if win:
            reason = "見送り正解"
        else:
            reason = f"見送り中に{actual_direction}方向へ動いた"

    result = "WIN" if win else "LOSE"

    price_diff = result_close - entry_close

    append_history({
        "id": pending["id"],
        "entry_time": pending["entry_time_jst"],
        "judge_time": result_time.tz_convert(
            ZoneInfo("Asia/Tokyo")
        ).isoformat(),
        "signal": signal,
        "actual_direction": actual_direction,
        "entry_close": entry_close,
        "result_close": result_close,
        "price_diff": round(price_diff, 6),
        "up_prob": pending["up_prob"],
        "down_prob": pending["down_prob"],
        "confidence": pending["confidence"],
        "delay_minutes": pending.get("delay_minutes", ""),
        "result": result
    })

    report = make_report_text()

    message = f"""
📊 BO_AI 採点結果

ID: {pending["id"]}

AI判断 : {signal}
実際 : {actual_direction}

エントリー : {entry_close:.3f}
判定 : {result_close:.3f}

価格差 : {price_diff:+.3f}

結果 : {"✅ 勝ち" if win else "❌ 負け"}

理由 : {reason}

{report}
"""

    send_telegram(message)

    clear_pending()

    return win
