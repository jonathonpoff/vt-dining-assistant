import requests

def scrape_hours(date_str):
    url = f"https://apps.students.vt.edu/hours/Api/NonRestricted/UnitsOpenOnDay/Date/{date_str}"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/123.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://dining.vt.edu/",
        "Origin": "https://dining.vt.edu",
    }

    r = requests.get(url, headers=headers)
    print("Status:", r.status_code)
    print("URL:", r.url)
    print("Text:", r.text[:300])
    r.raise_for_status()
    return r.json()
