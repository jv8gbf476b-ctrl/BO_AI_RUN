"""
BO_AI v4
report.py
勝率レポート
"""

from history import load_history


def make_report_text():
    df = load_history()

    if df.empty:
        return "📊 成績: まだ記録なし"

    total = len(df)

    wins = len(df[df["result"] == "WIN"])
    losses = len(df[df["result"] == "LOSE"])

    win_rate = wins / total * 100 if total else 0

    report = f"""
📊 BO_AI 成績

累計 : {total}戦
勝ち : {wins}
負け : {losses}
勝率 : {win_rate:.1f}%

"""

    for signal in ["HIGH", "LOW", "SKIP"]:

        signal_df = df[df["signal"] == signal]

        if signal_df.empty:
            continue

        signal_total = len(signal_df)
        signal_win = len(signal_df[signal_df["result"] == "WIN"])

        signal_rate = signal_win / signal_total * 100

        report += (
            f"{signal} : "
            f"{signal_win}/{signal_total} "
            f"({signal_rate:.1f}%)\n"
        )

    return report
