# app/state.py
cached_hours = {}

try:
    with open("normalized_hours.json", "r") as f:
        cached_hours = json.load(f)
except FileNotFoundError:
        cached_hours = {}