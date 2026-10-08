# Task Productivity & Completion Analysis System — P60

**Student:** Bhadaniya Vasu Atulbhai  
**Project No.:** P60  
**Domain:** Productivity

## Problem Statement
A student manages many tasks but wants to understand completion patterns, overdue work and how productive they are across different categories.

## Objective
Develop an application that manages tasks and provides productivity analysis.

## Functional Requirements Covered
- Maintain task records
- Track status and deadlines
- Search and filter tasks
- Update and delete tasks
- Mark tasks completed
- Calculate completion, pending and overdue statistics
- Compare categories
- Compare time periods
- Generate meaningful visual reports

## Technical Requirements Covered
- Python functions and data structures
- File handling using CSV
- More than 3 user-defined modules
- NumPy and Pandas
- Tkinter GUI
- Matplotlib visualizations
- Input validation
- Exception handling

## Installation

1. Install Python 3.10+.
2. Open a terminal in this folder.
3. Run:
   `pip install -r requirements.txt`
4. Run:
   `python main.py`

Tkinter normally comes with Python on Windows. On Linux, install the system Tk package if required.

## Project Modules

- `main.py` — Tkinter application and user interface
- `task_manager.py` — CRUD operations and filtering
- `data_handler.py` — CSV persistent storage
- `analysis.py` — Pandas/NumPy productivity analysis
- `validation.py` — input validation
- `reports.py` — Matplotlib visual reports

## Data

Tasks are stored in `data/tasks.csv`.

## Reports

Generated charts are stored in `reports/`.

## Suggested Demo

1. Add 8–15 tasks from different categories.
2. Use different priorities and deadlines.
3. Mark some tasks as completed.
4. Demonstrate search and filters.
5. Open Productivity Analysis.
6. Generate all reports.
7. Explain category and monthly productivity comparisons.
