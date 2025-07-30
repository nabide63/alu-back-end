#!/usr/bin/python3

"""This module downloads from an API (JSONPlaceholder) and prints the data."""

import json
import requests
import sys

if __name__ == "__main__":
    raw_user_data = requests.get(
        f"https://jsonplaceholder.typicode.com/users")
    raw_todo_data = requests.get(
        f"https://jsonplaceholder.typicode.com/todos")

    if raw_todo_data.status_code != 200 or raw_user_data.status_code != 200:
        print("Error: Failed to retrieve data from API.")
        sys.exit(1)

    user_json = raw_user_data.json()
    todo_json = raw_todo_data.json()
    todos = {}
    for user in user_json:
        user_todos = [
            {
                "username": user['username'],
                "task": todo['title'],
                "completed": todo['completed']
            }
            for todo in todo_json if todo['userId'] == user['id']
        ]
        todos.setdefault(str(user['id']), user_todos)

    with open("todo_all_employees.json", "w", newline="") as json_file:
        json.dump(todos, json_file, indent=4)
