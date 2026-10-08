from pathlib import Path
import matplotlib.pyplot as plt
from analysis import ProductivityAnalyzer

BASE_DIR = Path(__file__).resolve().parent
REPORT_DIR = BASE_DIR / "reports"
REPORT_DIR.mkdir(exist_ok=True)

analyzer = ProductivityAnalyzer()

def generate_status_report(df):
    stats = analyzer.summary(df)
    labels = ["Completed", "Pending", "Overdue"]
    values = [stats["completed"], stats["pending"], stats["overdue"]]

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.bar(labels, values)
    ax.set_title("Task Status Distribution")
    ax.set_ylabel("Number of Tasks")
    ax.set_xlabel("Status")
    fig.tight_layout()
    path = REPORT_DIR / "task_status_report.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return str(path)

def generate_category_report(df):
    cat = analyzer.category_analysis(df)
    if cat.empty:
        raise ValueError("Add tasks before generating category analysis.")

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(cat["Category"], cat["CompletionRate"])
    ax.set_title("Category-wise Productivity / Completion Rate")
    ax.set_ylabel("Completion Rate (%)")
    ax.set_xlabel("Category")
    ax.set_ylim(0, 100)
    ax.tick_params(axis="x", rotation=25)
    fig.tight_layout()
    path = REPORT_DIR / "category_productivity_report.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return str(path)

def generate_monthly_report(df):
    monthly = analyzer.monthly_analysis(df)
    if monthly.empty:
        raise ValueError("Add tasks with valid dates before generating monthly analysis.")

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(monthly["Month"], monthly["CompletionRate"], marker="o")
    ax.set_title("Monthly Productivity Trend")
    ax.set_ylabel("Completion Rate (%)")
    ax.set_xlabel("Month")
    ax.set_ylim(0, 100)
    ax.tick_params(axis="x", rotation=25)
    fig.tight_layout()
    path = REPORT_DIR / "monthly_productivity_report.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return str(path)
