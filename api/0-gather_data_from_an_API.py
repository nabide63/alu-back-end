#!/usr/bin/python3
"""
Script to fetch and display employee TODO list progress from a REST API
"""

import requests
import sys


def get_employee_todo_progress(employee_id):
    """
    Fetch and display TODO list progress for a given employee ID

    Args:
        employee_id (int): The ID of the employee
    """
    # API endpoints
    user_url = f"https://jsonplaceholder.typicode.com/users/{employee_id}"
    todos_url = (
        f"https://jsonplaceholder.typicode.com/users/{employee_id}/todos"
    )

    # Fetch user data
    user_response = requests.get(user_url)
    if user_response.status_code != 200:
        print(f"Error: Employee ID {employee_id} not found")
        return

    user_data = user_response.json()
    employee_name = user_data.get("name")

    # Fetch todos data
    todos_response = requests.get(todos_url)
    if todos_response.status_code != 200:
        print(f"Error: Unable to fetch TODOs for ID {employee_id}")
        return
    todos_data = todos_response.json()

    # Calculate completed and total tasks
    total_tasks = len(todos_data)
    done_tasks = sum(1 for task in todos_data if task.get("completed"))

    # Print employee progress with exact format
    print("Employee %s is done with tasks(%d/%d):" % (
        employee_name, done_tasks, total_tasks))

    # Print completed task titles with exact formatting
    for task in todos_data:
        if task.get("completed"):
            print("\t %s" % task.get("title"))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 0-gather_data_from_an_API.py <employee_id>")
        sys.exit(1)

    try:
        employee_id = int(sys.argv[1])
        get_employee_todo_progress(employee_id)
    except ValueError:
        print("Error: Employee ID must be an integer")
        sys.exit(1)