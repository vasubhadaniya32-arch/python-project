from datetime import date
from data_handler import load_tasks, save_tasks, COLUMNS

class TaskManager:
    def __init__(self):
        self.ensure_data()

    def ensure_data(self):
        load_tasks()

    def get_dataframe(self):
        df = load_tasks()
        if not df.empty:
            today = date.today().isoformat()
            df["DisplayStatus"] = df.apply(
                lambda r: "Overdue"
                if r["Status"] != "Completed" and r["Deadline"] and r["Deadline"] < today
                else r["Status"],
                axis=1
            )
        else:
            df["DisplayStatus"] = []
        return df

    def next_id(self):
        df = load_tasks()
        if df.empty:
            return "1"
        nums = []
        for value in df["TaskID"].tolist():
            try:
                nums.append(int(value))
            except (ValueError, TypeError):
                pass
        return str(max(nums, default=0) + 1)

    def add_task(self, data):
        df = load_tasks()
        data["TaskID"] = self.next_id()
        data["StartDate"] = date.today().isoformat()
        data["CompletionDate"] = ""
        row = {c: data.get(c, "") for c in COLUMNS}
        df.loc[len(df)] = row
        save_tasks(df)

    def update_task(self, task_id, data):
        df = load_tasks()
        matches = df.index[df["TaskID"].astype(str) == str(task_id)].tolist()
        if not matches:
            raise ValueError("Task ID not found.")
        idx = matches[0]
        old_completion = df.at[idx, "CompletionDate"]
        data["TaskID"] = str(task_id)
        data["StartDate"] = df.at[idx, "StartDate"]
        if data["Status"] == "Completed" and not data["CompletionDate"]:
            data["CompletionDate"] = old_completion or date.today().isoformat()
        if data["Status"] != "Completed":
            data["CompletionDate"] = ""
        for c in COLUMNS:
            df.at[idx, c] = data.get(c, "")
        save_tasks(df)

    def delete_task(self, task_id):
        df = load_tasks()
        new_df = df[df["TaskID"].astype(str) != str(task_id)].copy()
        if len(new_df) == len(df):
            raise ValueError("Task ID not found.")
        save_tasks(new_df)

    def complete_task(self, task_id):
        df = load_tasks()
        matches = df.index[df["TaskID"].astype(str) == str(task_id)].tolist()
        if not matches:
            raise ValueError("Task ID not found.")
        idx = matches[0]
        df.at[idx, "Status"] = "Completed"
        df.at[idx, "CompletionDate"] = date.today().isoformat()
        save_tasks(df)

    def apply_filters(self, df, search="", category="All", status="All", priority="All"):
        result = df.copy()
        if result.empty:
            return result

        if search.strip():
            key = search.strip().lower()
            result = result[result["TaskName"].str.lower().str.contains(key, na=False)]

        if category != "All":
            result = result[result["Category"] == category]

        if priority != "All":
            result = result[result["Priority"] == priority]

        if status != "All":
            result = result[result["DisplayStatus"] == status]

        return result
