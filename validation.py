from datetime import datetime

VALID_CATEGORIES = ["Study","Project","Personal","Work","Exercise","College","Other"]
VALID_PRIORITIES = ["High","Medium","Low"]
VALID_STATUSES = ["Pending","Completed"]

def validate_task_input(data, for_update=False):
    if not data["TaskName"]:
        raise ValueError("Task name cannot be empty.")

    if len(data["TaskName"]) > 100:
        raise ValueError("Task name must be 100 characters or fewer.")

    if data["Category"] not in VALID_CATEGORIES:
        raise ValueError("Please select a valid category.")

    if data["Priority"] not in VALID_PRIORITIES:
        raise ValueError("Please select a valid priority.")

    if data["Status"] not in VALID_STATUSES:
        raise ValueError("Please select a valid status.")

    if not data["Deadline"]:
        raise ValueError("Deadline is required.")

    try:
        deadline = datetime.strptime(data["Deadline"], "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Deadline must use YYYY-MM-DD format.")

    if data["Description"] and len(data["Description"]) > 300:
        raise ValueError("Description must be 300 characters or fewer.")

    return True
