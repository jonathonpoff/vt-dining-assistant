import requests
from datetime import date

BACKEND_URL = "https://your-backend-url.com/admin/update_hours"
SECRET = "your-secret-token"

def fetch_hours_for_today():
    today = date.today().strftime("%Y-%m-%d")
    url = f"https://apps.students.vt.edu/hours/Api/NonRestricted/UnitsOpenOnDay/Date/{today}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def normalize_hours(raw):
    normalized = []
    for unit in raw:
        normalized.append({
            "unit_id": unit.get("id"),
            "unit_name": unit.get("name"),
            "logo_url": unit.get("logo", {}).get("url"),
            "urls": unit.get("urls", []),
            "hours": unit.get("hours", []),
        })
    return normalized

def upload_to_backend(data):
    headers = {"X-Admin-Token": SECRET}
    response = requests.post(BACKEND_URL, json=data, headers=headers)
    response.raise_for_status()
    print("Upload successful:", response.json())

if __name__ == "__main__":
    raw = fetch_hours_for_today()
    normalized = normalize_hours(raw)
    upload_to_backend(normalized)
