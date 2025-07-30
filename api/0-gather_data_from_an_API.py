#!/usr/bin/python3

"""This module downloads from an API (JSONPlaceholder) and prints the data."""

import requests
import sys

if __name__ == "__main__":
    employer_number = sys.argv[1]
    raw_user_data = requests.get(
        f"https://jsonplaceholder.typicode.com/users?id={employer_number}")
    raw_todo_data = requests.get(
        f"https://jsonplaceholder.typicode.com/todos?userId={employer_number}")

    if raw_todo_data.status_code != 200 or raw_user_data.status_code != 200:
        print("Error: Failed to retrieve data from API.")
        sys.exit(1)

    user_json = raw_user_data.json()
    todo_json = raw_todo_data.json()

    if not user_json:
        print(f"Error: No user found with ID {employer_number}")
        sys.exit(1)

    user_name = user_json[0]["name"]
    todo_done = [x for x in todo_json if x['completed'] is True]
    print(
        "Employee {} is done with tasks({}/{}):"
        .format(user_name, len(todo_done), len(todo_json))
    )
    for todo in todo_done:
        print(f"\t {todo['title']}")
