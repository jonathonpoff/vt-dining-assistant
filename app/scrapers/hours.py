import requests

def scrape_hours():
    url = "https://apps.students.vt.edu/hours/fwa/uaMenu.json"
    data = requests.get(url).json()
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
