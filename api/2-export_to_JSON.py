#!/usr/bin/python3

"""This module downloads from an api (jsonplaceholder api)
 and stores it in a json file"""
import json
import requests
import sys


if __name__ == "__main__":
    employer_number = sys.argv[1]
    raw_user_data = requests.get(
        f"https://jsonplaceholder.typicode.com/users?id={employer_number}")
    raw_todo_data = requests.get(
        f"https://jsonplaceholder.typicode.com/todos?userId={employer_number}")
    user_json = raw_user_data.json()
    todo_json = raw_todo_data.json()

    username = user_json[0]["username"]
    formatted_json = {employer_number: [
        {
            "task": todo["title"],
            "completed": todo["completed"],
            "username": username
        } for todo in todo_json]}
    filename = f"{employer_number}.json"
    with open(filename, "w", newline="") as file:
        json.dump(formatted_json, file, indent=4)
