"""
BO_AI v5.1
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

    price_diff = result_close - entry_close

    if signal == "SKIP":
        result = "NO_TRADE"
        win = None

        if actual_direction == "FLAT":
            reason = "見送り。価格はほぼ動かず"
        else:
            reason = f"見送り中に{actual_direction}へ動いた"

    else:
        if signal == actual_direction:
            result = "WIN"
            win = True
            reason = "AI予測成功"
        else:
            result = "LOSE"
            win = False
            reason = "AI予測失敗"

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
        "result": result,
    })

    report = make_report_text()

    if result == "NO_TRADE":
        result_text = "⚪ 見送り"
    elif result == "WIN":
        result_text = "✅ 勝ち"
    else:
        result_text = "❌ 負け"

    message = f"""
📊 BO_AI 採点結果

ID: {pending['id']}

AI判断 : {signal}
実際 : {actual_direction}

エントリー : {entry_close:.3f}
判定 : {result_close:.3f}

価格差 : {price_diff:+.3f}

結果 : {result_text}

理由 : {reason}

{report}
"""

    send_telegram(message)

    clear_pending()

    return win
