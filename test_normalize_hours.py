import json

with open("raw_hours.json") as f:
    raw = json.load(f)

print("Loaded", len(raw), "units from raw_hours.json")

def normalize_unit(unit):
    # Extract URLs
    about_url = None
    menu_url = None

    for u in unit.get("urls", []):
        label = u.get("label", "").lower()
        if "about" in label:
            about_url = u["url"]
        if "menu" in label:
            menu_url = u["url"]

    # Extract hours blocks
    hours = []
    for h in unit.get("hours", []):
        hours.append({
            "label": h.get("label"),
            "open_time": h.get("open_time")[:5],   # "07:00"
            "close_time": h.get("close_time")[:5]  # "14:00"
        })

    return {
        "unit_id": unit["id"],
        "name": unit["name"],
        "about_url": about_url,
        "menu_url": menu_url,
        "hours": hours
    }

normalized = [normalize_unit(u) for u in raw]

print("Normalized", len(normalized), "units")
print("Example normalized unit:")
print(json.dumps(normalized[0], indent=2))

with open("normalized_hours.json", "w") as f:
    json.dump(normalized, f, indent=2)

print("Saved normalized_hours.json")
