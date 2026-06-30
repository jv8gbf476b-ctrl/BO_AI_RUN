"""
BO_AI v5.2
report.py
成績レポート・分析
"""

from history import load_history


def get_trade_df(df):
    if df.empty:
        return df

    return df[df["result"] != "NO_TRADE"]


def calc_win_rate(df):
    if df.empty:
        return 0, 0, 0, 0.0

    trade_df = get_trade_df(df)

    if trade_df.empty:
        return 0, 0, 0, 0.0

    total = len(trade_df)
    wins = len(trade_df[trade_df["result"] == "WIN"])
    losses = len(trade_df[trade_df["result"] == "LOSE"])
    win_rate = wins / total * 100 if total else 0.0

    return total, wins, losses, win_rate


def confidence_rank(confidence):
    confidence = float(confidence)

    if confidence >= 0.90:
        return "★★★★★"
    if confidence >= 0.80:
        return "★★★★☆"
    if confidence >= 0.70:
        return "★★★☆☆"
    if confidence >= 0.60:
        return "★★☆☆☆"
    return "★☆☆☆☆"


def confidence_band(confidence):
    confidence = float(confidence)

    if confidence >= 0.90:
        return "90%以上"
    if confidence >= 0.80:
        return "80〜90%"
    if confidence >= 0.75:
        return "75〜80%"
    if confidence >= 0.70:
        return "70〜75%"
    if confidence >= 0.60:
        return "60〜70%"
    return "60%未満"


def make_signal_report(df):
    text = "\n📌 判定別\n"

    for signal in ["HIGH", "LOW", "SKIP"]:
        signal_df = df[df["signal"] == signal]

        if signal_df.empty:
            continue

        if signal == "SKIP":
            text += f"SKIP : {len(signal_df)}回 見送り\n"
            continue

        total, wins, losses, win_rate = calc_win_rate(signal_df)

        text += (
            f"{signal} : "
            f"{total}戦 "
            f"{wins}勝 "
            f"{losses}敗 "
            f"勝率{win_rate:.1f}%\n"
        )

    return text


def make_rank_report(df):
    if "confidence" not in df.columns:
        return ""

    data = get_trade_df(df.copy())

    if data.empty:
        return "\n⭐ 信頼度別\nエントリー記録なし\n"

    data["rank"] = data["confidence"].apply(confidence_rank)

    text = "\n⭐ 信頼度別\n"

    for rank in ["★★★★★", "★★★★☆", "★★★☆☆", "★★☆☆☆", "★☆☆☆☆"]:
        rank_df = data[data["rank"] == rank]

        if rank_df.empty:
            continue

        total, wins, losses, win_rate = calc_win_rate(rank_df)
        avg_conf = rank_df["confidence"].mean() * 100

        text += (
            f"{rank} : "
            f"{total}戦 "
            f"{wins}勝 "
            f"{losses}敗 "
            f"勝率{win_rate:.1f}% "
            f"(平均{avg_conf:.1f}%)\n"
        )

    return text


def make_confidence_band_report(df):
    if "confidence" not in df.columns:
        return ""

    data = get_trade_df(df.copy())

    if data.empty:
        return "\n🎯 確率帯別\nエントリー記録なし\n"

    data["band"] = data["confidence"].apply(confidence_band)

    text = "\n🎯 確率帯別\n"

    for band in [
        "90%以上",
        "80〜90%",
        "75〜80%",
        "70〜75%",
        "60〜70%",
        "60%未満",
    ]:
        band_df = data[data["band"] == band]

        if band_df.empty:
            continue

        total, wins, losses, win_rate = calc_win_rate(band_df)

        text += (
            f"{band} : "
            f"{total}戦 "
            f"{wins}勝 "
            f"{losses}敗 "
            f"勝率{win_rate:.1f}%\n"
        )

    return text


def make_recent_report(df, count):
    recent = get_trade_df(df.tail(count))

    if recent.empty:
        return f"""
🕒 直近{count}戦
エントリー記録なし
"""

    total, wins, losses, win_rate = calc_win_rate(recent)

    return f"""
🕒 直近{count}戦
{total}戦 {wins}勝 {losses}敗
勝率 : {win_rate:.1f}%
"""


def make_report_text():
    df = load_history()

    if df.empty:
        return "📊 成績: まだ記録なし"

    total, wins, losses, win_rate = calc_win_rate(df)
    skip_count = len(df[df["result"] == "NO_TRADE"])

    report = f"""
📊 BO_AI 成績分析

累計エントリー : {total}戦
勝ち : {wins}
負け : {losses}
勝率 : {win_rate:.1f}%
見送り : {skip_count}回
"""

    report += make_signal_report(df)
    report += make_rank_report(df)
    report += make_confidence_band_report(df)

    report += make_recent_report(df, 20)
    report += make_recent_report(df, 50)
    report += make_recent_report(df, 100)

    return report
