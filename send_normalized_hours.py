import json
import requests

API_URL = "https://vt-dining-assistant-5ik5.onrender.com/admin/update_hours"
ADMIN_TOKEN = "your-secret-token"   # same as HOURS_SECRET in main.py

# Load normalized data
with open("normalized_hours.json") as f:
    units = json.load(f)

# Send to your backend
response = requests.post(
    API_URL,
    json=units,
    headers={"X-Admin-Token": ADMIN_TOKEN}
)

print("Status:", response.status_code)
print("Response:", response.text)
