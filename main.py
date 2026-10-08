import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from task_manager import TaskManager
from analysis import ProductivityAnalyzer
from validation import validate_task_input
from reports import generate_status_report, generate_category_report, generate_monthly_report

class TaskProductivityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Productivity & Completion Analysis System")
        self.root.geometry("1250x760")
        self.root.minsize(1050, 650)

        self.manager = TaskManager()
        self.analyzer = ProductivityAnalyzer()

        self.vars = {
            "task_id": tk.StringVar(),
            "task_name": tk.StringVar(),
            "category": tk.StringVar(value="Study"),
            "priority": tk.StringVar(value="Medium"),
            "deadline": tk.StringVar(),
            "status": tk.StringVar(value="Pending"),
            "search": tk.StringVar(),
            "filter_category": tk.StringVar(value="All"),
            "filter_status": tk.StringVar(value="All"),
            "filter_priority": tk.StringVar(value="All"),
        }

        self.build_style()
        self.build_ui()
        self.refresh_all()

    def build_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Title.TLabel", font=("Segoe UI", 20, "bold"))
        style.configure("Card.TLabel", font=("Segoe UI", 16, "bold"))
        style.configure("Small.TLabel", font=("Segoe UI", 9))
        style.configure("Treeview", rowheight=28, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"))

    def build_ui(self):
        header = ttk.Frame(self.root, padding=(15, 12))
        header.pack(fill="x")
        ttk.Label(header, text="TASK PRODUCTIVITY & COMPLETION ANALYSIS SYSTEM",
                  style="Title.TLabel").pack(side="left")
        ttk.Label(header, text="P60 • Bhadaniya Vasu Atulbhai",
                  font=("Segoe UI", 10, "bold")).pack(side="right")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        self.dashboard_tab = ttk.Frame(self.notebook, padding=12)
        self.tasks_tab = ttk.Frame(self.notebook, padding=12)
        self.analysis_tab = ttk.Frame(self.notebook, padding=12)
        self.reports_tab = ttk.Frame(self.notebook, padding=12)

        self.notebook.add(self.dashboard_tab, text="Dashboard")
        self.notebook.add(self.tasks_tab, text="Task Management")
        self.notebook.add(self.analysis_tab, text="Productivity Analysis")
        self.notebook.add(self.reports_tab, text="Visual Reports")

        self.build_dashboard()
        self.build_tasks()
        self.build_analysis()
        self.build_reports()

    def build_dashboard(self):
        for c in range(5):
            self.dashboard_tab.columnconfigure(c, weight=1)

        self.card_values = {}
        cards = [
            ("Total Tasks", "total"),
            ("Completed", "completed"),
            ("Pending", "pending"),
            ("Overdue", "overdue"),
            ("Completion Rate", "rate"),
        ]
        for i, (title, key) in enumerate(cards):
            frame = ttk.LabelFrame(self.dashboard_tab, text=title, padding=18)
            frame.grid(row=0, column=i, padx=6, pady=8, sticky="nsew")
            label = ttk.Label(frame, text="0", style="Card.TLabel", anchor="center")
            label.pack(fill="both", expand=True)
            self.card_values[key] = label

        info = ttk.LabelFrame(self.dashboard_tab, text="Project Requirements Covered", padding=15)
        info.grid(row=1, column=0, columnspan=5, sticky="nsew", padx=6, pady=12)
        self.dashboard_tab.rowconfigure(1, weight=1)

        text = (
            "✓ Task management: add, view, search, filter, update, delete and complete tasks\n"
            "✓ Productivity analysis: completion, pending and overdue statistics\n"
            "✓ Category and time-period comparison\n"
            "✓ Persistent CSV file storage with Python file handling\n"
            "✓ Pandas and NumPy data analysis\n"
            "✓ Tkinter GUI with validation and exception handling\n"
            "✓ Matplotlib visual reports (status, category and monthly productivity)\n"
            "✓ More than 3 user-defined modules"
        )
        ttk.Label(info, text=text, font=("Segoe UI", 12), justify="left").pack(anchor="w")

    def build_tasks(self):
        form = ttk.LabelFrame(self.tasks_tab, text="Task Details", padding=12)
        form.pack(fill="x")

        labels = [
            ("Task ID", "task_id"), ("Task Name", "task_name"),
            ("Category", "category"), ("Priority", "priority"),
            ("Deadline (YYYY-MM-DD)", "deadline"), ("Status", "status")
        ]
        for i, (label, key) in enumerate(labels):
            r, c = divmod(i, 4)
            ttk.Label(form, text=label).grid(row=r*2, column=c, padx=6, pady=(4, 2), sticky="w")
            if key == "category":
                widget = ttk.Combobox(form, textvariable=self.vars[key],
                                      values=["Study","Project","Personal","Work","Exercise","College","Other"],
                                      state="readonly", width=18)
            elif key == "priority":
                widget = ttk.Combobox(form, textvariable=self.vars[key],
                                      values=["High","Medium","Low"], state="readonly", width=18)
            elif key == "status":
                widget = ttk.Combobox(form, textvariable=self.vars[key],
                                      values=["Pending","Completed"], state="readonly", width=18)
            else:
                widget = ttk.Entry(form, textvariable=self.vars[key], width=22)
            widget.grid(row=r*2+1, column=c, padx=6, pady=(0, 6), sticky="ew")

        desc_frame = ttk.Frame(self.tasks_tab)
        desc_frame.pack(fill="x", pady=(2, 8))
        ttk.Label(desc_frame, text="Description").pack(side="left", padx=(0, 8))
        self.description_var = tk.StringVar()
        ttk.Entry(desc_frame, textvariable=self.description_var).pack(
            side="left", fill="x", expand=True
        )

        buttons = ttk.Frame(self.tasks_tab)
        buttons.pack(fill="x", pady=10)
        actions = [
            ("Add Task", self.add_task), ("Update Task", self.update_task),
            ("Delete Task", self.delete_task), ("Mark Completed", self.complete_task),
            ("Clear Form", self.clear_form)
        ]
        for text, command in actions:
            ttk.Button(buttons, text=text, command=command,
                       style="Accent.TButton").pack(side="left", padx=4)

        filters = ttk.LabelFrame(self.tasks_tab, text="Search & Filter", padding=10)
        filters.pack(fill="x", pady=(0, 10))
        ttk.Label(filters, text="Search").pack(side="left")
        ttk.Entry(filters, textvariable=self.vars["search"], width=25).pack(side="left", padx=5)
        ttk.Button(filters, text="Search", command=self.refresh_tasks).pack(side="left", padx=4)
        ttk.Button(filters, text="Reset", command=self.reset_filters).pack(side="left", padx=4)

        for key, title, values in [
            ("filter_category", "Category", ["All","Study","Project","Personal","Work","Exercise","College","Other"]),
            ("filter_status", "Status", ["All","Pending","Completed","Overdue"]),
            ("filter_priority", "Priority", ["All","High","Medium","Low"])
        ]:
            ttk.Label(filters, text=title).pack(side="left", padx=(15, 3))
            ttk.Combobox(filters, textvariable=self.vars[key], values=values,
                         state="readonly", width=12).pack(side="left")
        ttk.Button(filters, text="Apply Filters", command=self.refresh_tasks).pack(side="left", padx=8)

        table_frame = ttk.Frame(self.tasks_tab)
        table_frame.pack(fill="both", expand=True)

        columns = ("id","name","category","priority","deadline","status","completion_date","description")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
        headings = {
            "id":"ID","name":"Task Name","category":"Category","priority":"Priority",
            "deadline":"Deadline","status":"Status","completion_date":"Completed On","description":"Description"
        }
        widths = {"id":50,"name":190,"category":100,"priority":80,"deadline":100,"status":95,"completion_date":110,"description":240}
        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=widths[col], anchor="center" if col != "description" else "w")
        self.tree.pack(side="left", fill="both", expand=True)
        scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scroll.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.bind("<<TreeviewSelect>>", self.on_select_task)

    def build_analysis(self):
        top = ttk.Frame(self.analysis_tab)
        top.pack(fill="x")
        ttk.Button(top, text="Refresh Analysis", command=self.refresh_analysis).pack(side="left")
        ttk.Button(top, text="Open Task Management", command=lambda: self.notebook.select(self.tasks_tab)).pack(side="left", padx=8)

        self.analysis_text = tk.Text(self.analysis_tab, height=20, font=("Consolas", 11), wrap="word")
        self.analysis_text.pack(fill="both", expand=True, pady=12)

    def build_reports(self):
        ttk.Label(self.reports_tab,
                  text="Generate meaningful visual reports required by the project specification.",
                  font=("Segoe UI", 12)).pack(anchor="w", pady=(0, 15))

        buttons = [
            ("Task Status Report", self.make_status_report),
            ("Category Productivity Report", self.make_category_report),
            ("Monthly Productivity Report", self.make_monthly_report),
            ("Generate All Reports", self.make_all_reports),
        ]
        for text, command in buttons:
            ttk.Button(self.reports_tab, text=text, command=command,
                       style="Accent.TButton").pack(fill="x", pady=6)

        ttk.Label(self.reports_tab,
                  text="Generated PNG files are stored in the reports/ folder.",
                  style="Small.TLabel").pack(anchor="w", pady=15)

    def add_task(self):
        try:
            data = self.get_form_data()
            validate_task_input(data, for_update=False)
            self.manager.add_task(data)
            messagebox.showinfo("Success", "Task added successfully.")
            self.clear_form()
            self.refresh_all()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_task(self):
        try:
            data = self.get_form_data()
            validate_task_input(data, for_update=True)
            self.manager.update_task(data["TaskID"], data)
            messagebox.showinfo("Success", "Task updated successfully.")
            self.clear_form()
            self.refresh_all()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_task(self):
        try:
            task_id = self.vars["task_id"].get().strip()
            if not task_id:
                raise ValueError("Select a task or enter a Task ID.")
            if not messagebox.askyesno("Confirm", f"Delete task {task_id}?"):
                return
            self.manager.delete_task(task_id)
            messagebox.showinfo("Success", "Task deleted successfully.")
            self.clear_form()
            self.refresh_all()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def complete_task(self):
        try:
            task_id = self.vars["task_id"].get().strip()
            if not task_id:
                raise ValueError("Select a task first.")
            self.manager.complete_task(task_id)
            messagebox.showinfo("Success", "Task marked as completed.")
            self.refresh_all()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def get_form_data(self):
        return {
            "TaskID": self.vars["task_id"].get().strip(),
            "TaskName": self.vars["task_name"].get().strip(),
            "Category": self.vars["category"].get().strip(),
            "Priority": self.vars["priority"].get().strip(),
            "Deadline": self.vars["deadline"].get().strip(),
            "Status": self.vars["status"].get().strip(),
            "CompletionDate": "",
            "Description": self.description_var.get().strip()
        }

    def clear_form(self):
        self.vars["task_id"].set("")
        self.vars["task_name"].set("")
        self.vars["category"].set("Study")
        self.vars["priority"].set("Medium")
        self.vars["deadline"].set("")
        self.vars["status"].set("Pending")
        if hasattr(self, "description_var"):
            self.description_var.set("")

    def reset_filters(self):
        self.vars["search"].set("")
        self.vars["filter_category"].set("All")
        self.vars["filter_status"].set("All")
        self.vars["filter_priority"].set("All")
        self.refresh_tasks()

    def on_select_task(self, event=None):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0], "values")
        self.vars["task_id"].set(values[0])
        self.vars["task_name"].set(values[1])
        self.vars["category"].set(values[2])
        self.vars["priority"].set(values[3])
        self.vars["deadline"].set(values[4])
        self.vars["status"].set("Pending" if values[5] == "Overdue" else values[5])
        if not hasattr(self, "description_var"):
            self.description_var = tk.StringVar()
        self.description_var.set(values[7])

    def refresh_tasks(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        df = self.manager.get_dataframe()
        df = self.manager.apply_filters(
            df,
            search=self.vars["search"].get(),
            category=self.vars["filter_category"].get(),
            status=self.vars["filter_status"].get(),
            priority=self.vars["filter_priority"].get()
        )
        for _, row in df.iterrows():
            self.tree.insert("", "end", values=(
                row["TaskID"], row["TaskName"], row["Category"], row["Priority"],
                row["Deadline"], row["DisplayStatus"], row["CompletionDate"],
                row["Description"]
            ))

    def refresh_dashboard(self):
        stats = self.analyzer.summary(self.manager.get_dataframe())
        self.card_values["total"].config(text=str(stats["total"]))
        self.card_values["completed"].config(text=str(stats["completed"]))
        self.card_values["pending"].config(text=str(stats["pending"]))
        self.card_values["overdue"].config(text=str(stats["overdue"]))
        self.card_values["rate"].config(text=f'{stats["completion_rate"]:.1f}%')

    def refresh_analysis(self):
        df = self.manager.get_dataframe()
        text = self.analyzer.full_report(df)
        self.analysis_text.delete("1.0", "end")
        self.analysis_text.insert("1.0", text)

    def make_status_report(self):
        try:
            path = generate_status_report(self.manager.get_dataframe())
            messagebox.showinfo("Report Created", f"Saved:\n{path}")
        except Exception as e:
            messagebox.showerror("Report Error", str(e))

    def make_category_report(self):
        try:
            path = generate_category_report(self.manager.get_dataframe())
            messagebox.showinfo("Report Created", f"Saved:\n{path}")
        except Exception as e:
            messagebox.showerror("Report Error", str(e))

    def make_monthly_report(self):
        try:
            path = generate_monthly_report(self.manager.get_dataframe())
            messagebox.showinfo("Report Created", f"Saved:\n{path}")
        except Exception as e:
            messagebox.showerror("Report Error", str(e))

    def make_all_reports(self):
        try:
            df = self.manager.get_dataframe()
            paths = [
                generate_status_report(df),
                generate_category_report(df),
                generate_monthly_report(df)
            ]
            messagebox.showinfo("Reports Created", "\n".join(paths))
        except Exception as e:
            messagebox.showerror("Report Error", str(e))

    def refresh_all(self):
        self.refresh_tasks()
        self.refresh_dashboard()
        self.refresh_analysis()

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskProductivityApp(root)
    root.mainloop()
