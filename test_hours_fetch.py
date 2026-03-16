import requests
import json
from datetime import date

# Pick a date to test
today = date.today().strftime("%Y-%m-%d")

url = f"https://apps.students.vt.edu/hours/Api/NonRestricted/UnitsOpenOnDay/Date/{today}"

print("Fetching:", url)
response = requests.get(url)
response.raise_for_status()

data = response.json()

# Save to disk
with open("raw_hours.json", "w") as f:
    json.dump(data, f, indent=2)

print("Saved raw_hours.json with", len(data), "units")

with open("raw_hours.json") as f:
    loaded = json.load(f)

print("Loaded", len(loaded), "units from disk")
print("First unit keys:", loaded[0].keys())
