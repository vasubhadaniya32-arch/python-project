import numpy as np
import pandas as pd
from datetime import date

class ProductivityAnalyzer:
    def summary(self, df):
        total = len(df)
        completed = int((df["Status"] == "Completed").sum()) if total else 0
        pending = int((df["Status"] == "Pending").sum()) if total else 0
        overdue = int((df["DisplayStatus"] == "Overdue").sum()) if total else 0
        rate = (completed / total * 100) if total else 0
        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "overdue": overdue,
            "completion_rate": rate
        }

    def category_analysis(self, df):
        if df.empty:
            return pd.DataFrame(columns=["Category", "Total", "Completed", "CompletionRate"])
        grouped = df.groupby("Category").agg(
            Total=("TaskID", "count"),
            Completed=("Status", lambda x: (x == "Completed").sum())
        ).reset_index()
        grouped["CompletionRate"] = np.where(
            grouped["Total"] > 0,
            grouped["Completed"] / grouped["Total"] * 100,
            0
        )
        return grouped.sort_values("CompletionRate", ascending=False)

    def monthly_analysis(self, df):
        if df.empty:
            return pd.DataFrame(columns=["Month", "Total", "Completed", "CompletionRate"])
        temp = df.copy()
        temp["StartDate"] = pd.to_datetime(temp["StartDate"], errors="coerce")
        temp = temp.dropna(subset=["StartDate"])
        if temp.empty:
            return pd.DataFrame(columns=["Month", "Total", "Completed", "CompletionRate"])
        temp["Month"] = temp["StartDate"].dt.to_period("M").astype(str)
        grouped = temp.groupby("Month").agg(
            Total=("TaskID", "count"),
            Completed=("Status", lambda x: (x == "Completed").sum())
        ).reset_index()
        grouped["CompletionRate"] = grouped["Completed"] / grouped["Total"] * 100
        return grouped.sort_values("Month")

    def full_report(self, df):
        s = self.summary(df)
        lines = [
            "PRODUCTIVITY ANALYSIS",
            "=" * 70,
            f"Total Tasks        : {s['total']}",
            f"Completed Tasks    : {s['completed']}",
            f"Pending Tasks      : {s['pending']}",
            f"Overdue Tasks      : {s['overdue']}",
            f"Completion Rate    : {s['completion_rate']:.2f}%",
            "",
            "CATEGORY COMPARISON",
            "-" * 70
        ]
        cat = self.category_analysis(df)
        if cat.empty:
            lines.append("No category data available.")
        else:
            for _, r in cat.iterrows():
                lines.append(
                    f"{r['Category']:<15} Total={int(r['Total']):<4} "
                    f"Completed={int(r['Completed']):<4} Rate={r['CompletionRate']:.2f}%"
                )
            best = cat.iloc[0]
            worst = cat.iloc[-1]
            lines += [
                "",
                f"Highest completion category : {best['Category']} ({best['CompletionRate']:.2f}%)",
                f"Lowest completion category  : {worst['Category']} ({worst['CompletionRate']:.2f}%)"
            ]

        lines += ["", "MONTHLY COMPARISON", "-" * 70]
        monthly = self.monthly_analysis(df)
        if monthly.empty:
            lines.append("No monthly data available.")
        else:
            for _, r in monthly.iterrows():
                lines.append(
                    f"{r['Month']:<12} Total={int(r['Total']):<4} "
                    f"Completed={int(r['Completed']):<4} Rate={r['CompletionRate']:.2f}%"
                )
        return "\n".join(lines)
