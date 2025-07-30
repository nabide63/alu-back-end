#!/usr/bin/python3
"""
Fetches employee TODO list from JSONPlaceholder API and exports to JSON.
"""

import json
import requests
import sys


def export_employee_todo_json(employee_id):
    """
    Fetches employee TODO list and exports to JSON for a given employee ID.

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

    # Export to JSON
    filename = f"{user_id}.json"
    tasks_data = [
        {
            "task": task.get("title", ""),
            "completed": task.get("completed", False),
            "username": employee_name
        }
        for task in todos_data
    ]
    json_data = {str(user_id): tasks_data}
    with open(filename, mode='w') as file:
        json.dump(json_data, file)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 2-export_to_json.py <employee_id>")
        sys.exit(1)

    try:
        employee_id = int(sys.argv[1])
        export_employee_todo_json(employee_id)
    except ValueError:
        print("Error: Employee ID must be an integer")
        sys.exit(1)
