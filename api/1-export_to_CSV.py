#!/usr/bin/python3
"""This module downloads from an API (JSONPlaceholder) and prints the data."""

import csv
import requests
import sys


def get_employee_todo_progress(employee_id):
    """
    Fetch and display TODO list progress for a given employee ID, and export
    to CSV.

    Args:
        employee_id (int): The ID of the employee
    """
    # API endpoints
    user_url = f"https://jsonplaceholder.typicode.com/users/{employee_id}"
    todos_url = (
        f"https://jsonplaceholder.typicode.com/todos?userId={employee_id}"
    )

    # Fetch user data
    user_response = requests.get(user_url)
    if user_response.status_code != 200:
        print(f"Error: Employee ID {employee_id} not found")
        sys.exit(1)

    user_data = user_response.json()
    employee_name = user_data.get("name", "").strip()
    user_id = user_data.get("id")

    # Fetch todos data
    todos_response = requests.get(todos_url)
    if todos_response.status_code != 200:
        print(f"Error: Unable to fetch TODOs for ID {employee_id}")
        sys.exit(1)

    todos_data = todos_response.json()

    # Calculate completed and total tasks
    total_tasks = len(todos_data)
    done_tasks = sum(1 for todo in todos_data if todo.get("completed"))

    # Print employee progress with exact format
    print("Employee " + employee_name + " is done with tasks(" +
          str(done_tasks) + "/" + str(total_tasks) + "):")

    # Print completed task titles with exact formatting
    for todo in todos_data:
        if todo.get("completed"):
            print("\t " + todo.get("title"))

    # Export to CSV
    filename = f"{user_id}.csv"
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file, quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(["USER_ID", "USERNAME", "TASK_COMPLETED_STATUS",
                        "TASK_TITLE"])
        for todo in todos_data:
            writer.writerow([
                str(user_id),
                employee_name,
                str(todo.get("completed")).lower(),
                todo.get("title")
            ])


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 0-gather_data_from_an_api.py <employee_id>")
        sys.exit(1)

    try:
        employee_id = int(sys.argv[1])
        get_employee_todo_progress(employee_id)
    except ValueError:
        print("Error: Employee ID must be an integer")
        sys.exit(1)
