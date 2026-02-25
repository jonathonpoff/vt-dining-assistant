import re
from difflib import SequenceMatcher
from app.scrapers.hours import scrape_hours

# Cache so we don't hit the API every request
LOCATION_CACHE = None

def load_locations():
    global LOCATION_CACHE
    if LOCATION_CACHE is None:
        _, locations = scrape_hours()
        LOCATION_CACHE = locations
    return LOCATION_CACHE

def normalize(text):
    return re.sub(r"[^a-z0-9 ]", "", text.lower()).strip()

def fuzzy_ratio(a, b):
    return SequenceMatcher(None, a, b).ratio()

def match_location(user_message):
    msg = normalize(user_message)
    locations = load_locations()

    best = None
    best_score = 0

    for official_name, data in locations.items():
        # Compare to official name
        score = fuzzy_ratio(msg, normalize(official_name))
        if score > best_score:
            best = (official_name, data)
            best_score = score

        # Compare to aliases
        for alias in data["aliases"]:
            score = fuzzy_ratio(msg, normalize(alias))
            if score > best_score:
                best = (official_name, data)
                best_score = score

    if best_score < 0.45:
        return None

    name, data = best
    return {"name": name, "location_num": data["location_num"]}

def match_item(user_message):
    """
    Placeholder item matcher.
    Returns None for now until menu-based matching is implemented.
    """
    return None
