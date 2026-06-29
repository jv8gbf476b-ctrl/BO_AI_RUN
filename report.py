"""
BO_AI v4.8
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

    report += "📌 判定別\n"

    for signal in ["HIGH", "LOW", "SKIP"]:
        signal_df = df[df["signal"] == signal]

        if signal_df.empty:
            continue

        s_total, s_wins, s_losses, s_rate = calc_win_rate(signal_df)

        report += (
            f"{signal} : "
            f"{s_total}戦 "
            f"{s_wins}勝 "
            f"{s_losses}敗 "
            f"勝率{s_rate:.1f}%\n"
        )

    if "confidence" in df.columns:
        report += "\n⭐ 信頼度別\n"

        df = df.copy()
        df["rank"] = df["confidence"].apply(confidence_rank)

        for rank in ["★★★★★", "★★★★☆", "★★★☆☆", "★★☆☆☆", "★☆☆☆☆"]:
            rank_df = df[df["rank"] == rank]

            if rank_df.empty:
                continue

            r_total, r_wins, r_losses, r_rate = calc_win_rate(rank_df)

            report += (
                f"{rank} : "
                f"{r_total}戦 "
                f"{r_wins}勝 "
                f"{r_losses}敗 "
                f"勝率{r_rate:.1f}%\n"
            )

    recent = df.tail(20)

    if not recent.empty:
        r_total, r_wins, r_losses, r_rate = calc_win_rate(recent)

        report += f"""
\n🕒 直近20戦
{r_total}戦 {r_wins}勝 {r_losses}敗
勝率 : {r_rate:.1f}%
"""

    return report
