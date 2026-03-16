import requests

def scrape_hours():
    url = "https://apps.students.vt.edu/hours/fwa/uaMenu.json"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/123.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://dining.vt.edu/",
        "Origin": "https://dining.vt.edu",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Connection": "keep-alive",
    }

    response = requests.get(url, headers=headers, allow_redirects=True)
    
    print("Status:", response.status_code)
    print("Final URL:", response.url)
    print("Raw text:", response.text[:500])
    
    try:
        data = response.json()
    except Exception as e:
        print("JSON decode failed:", e)
        return{}
    
    print("Parsed JSON:", data)
    return data
    

    # Log non-200 responses
    if response.status_code != 200:
        print("Hours scraper failed:", response.status_code, response.text[:200])
        return {}

    try:
        data = response.json()
        print("Hours data:", data)
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
