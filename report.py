"""
BO_AI v4.9
report.py
成績レポート・分析
"""

from history import load_history


def calc_win_rate(df):
    if df.empty:
        return 0, 0, 0, 0.0

    total = len(df)
    wins = len(df[df["result"] == "WIN"])
    losses = len(df[df["result"] == "LOSE"])
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


def make_section_report(title, df):
    total, wins, losses, win_rate = calc_win_rate(df)

    return f"""
{title}
{total}戦 {wins}勝 {losses}敗
勝率 : {win_rate:.1f}%
"""


def make_signal_report(df):
    text = "\n📌 判定別\n"

    for signal in ["HIGH", "LOW", "SKIP"]:
        signal_df = df[df["signal"] == signal]

        if signal_df.empty:
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

    data = df.copy()
    data["rank"] = data["confidence"].apply(confidence_rank)

    text = "\n⭐ 信頼度別\n"

    for rank in ["★★★★★", "★★★★☆", "★★★☆☆", "★★☆☆☆", "★☆☆☆☆"]:
        rank_df = data[data["rank"] == rank]

        if rank_df.empty:
            continue

        total, wins, losses, win_rate = calc_win_rate(rank_df)

        text += (
            f"{rank} : "
            f"{total}戦 "
            f"{wins}勝 "
            f"{losses}敗 "
            f"勝率{win_rate:.1f}%\n"
        )

    return text


def make_recent_report(df, count):
    recent = df.tail(count)

    if recent.empty:
        return ""

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

    report = f"""
📊 BO_AI 成績分析

累計 : {total}戦
勝ち : {wins}
負け : {losses}
勝率 : {win_rate:.1f}%
"""

    report += make_signal_report(df)
    report += make_rank_report(df)

    report += make_recent_report(df, 20)
    report += make_recent_report(df, 50)
    report += make_recent_report(df, 100)

    return report
