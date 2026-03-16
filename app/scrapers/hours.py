import requests

def scrape_hours():
    url = "https://apps.students.vt.edu/hours/fwa/uaMenu.json"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(url, headers=headers)

    # Log non-200 responses
    if response.status_code != 200:
        print("Hours scraper failed:", response.status_code, response.text[:200])
        return {}

    try:
        data = response.json()
    except Exception as e:
        print("JSON decode failed:", e, response.text[:200])
        return {}

    hours = {}
    for location in data.get("locations", []):
        name = location.get("name")
        today = location.get("today", {})
        opens = today.get("open")
        closes = today.get("close")

        hours[name] = {
            "opens_at": opens,
            "closes_at": closes,
            "raw": today
        }

    return hours
