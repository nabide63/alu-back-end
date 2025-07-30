#!/usr/bin/python3
"""
Fetches employee TODO list from JSONPlaceholder API and exports to CSV.
"""

import csv
import requests
import sys


def export_employee_todo_csv(employee_id):
    """
    Fetches employee TODO list and exports to CSV for a given employee ID.

    Args:
        employee_id (int): The ID of the employee.
    """
    # API endpoints
    user_url = f"https://jsonplaceholder.typicode.com/users/{employee_id}"
    todos_url = f"https://jsonplaceholder.typicode.com/todos?userId={employee_id}"

    # Fetch user data
    user_response = requests.get(user_url)
    if user_response.status_code != 200:
        print(f"Error: Employee ID {employee_id} not found")
        return

    user_data = user_response.json()
    employee_name = user_data.get("name", "").strip()
    user_id = user_data.get("id", "")

    # Fetch todos data
    todos_response = requests.get(todos_url)
    if todos_response.status_code != 200:
        print(f"Error: Unable to fetch TODOs for ID {employee_id}")
        return
    todos_data = todos_response.json()

    # Print employee progress in exact format
    total_tasks = len(todos_data)
    done_tasks = sum(1 for task in todos_data if task.get("completed", False))
    print(f"Employee {employee_name} is done with tasks({done_tasks}/{total_tasks}):")
    for task in todos_data:
        if task.get("completed", False):
            print(f"\t {task.get('title', '')}")

    # Export to CSV
    filename = f"{user_id}.csv"
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file, quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(["USER_ID", "USERNAME", "TASK_COMPLETED_STATUS", "TASK_TITLE"])
        for task in todos_data:
            writer.writerow([
                str(user_id),
                employee_name,
                str(task.get("completed", False)).lower(),
                task.get("title", "")
            ])


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 1-export_to_csv.py <employee_id>")
        sys.exit(1)

    try:
        employee_id = int(sys.argv[1])
        export_employee_todo_csv(employee_id)
    except ValueError:
        print("Error: Employee ID must be an integer")
        sys.exit(1)
