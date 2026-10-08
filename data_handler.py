import csv
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "tasks.csv"

COLUMNS = [
    "TaskID", "TaskName", "Category", "Priority",
    "StartDate", "Deadline", "Status", "CompletionDate", "Description"
]

def ensure_data_file():
    DATA_DIR.mkdir(exist_ok=True)
    if not DATA_FILE.exists():
        with DATA_FILE.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(COLUMNS)

def load_tasks():
    ensure_data_file()
    try:
        return pd.read_csv(DATA_FILE, dtype=str).fillna("")
    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=COLUMNS)

def save_tasks(df):
    ensure_data_file()
    df = df.reindex(columns=COLUMNS).fillna("")
    df.to_csv(DATA_FILE, index=False, encoding="utf-8")
