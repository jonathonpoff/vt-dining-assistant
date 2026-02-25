from datetime import datetime
def get_open_locations(hours):
    now = datetime.now().strftime("%H:%M")
    open_now = []
    for name, info in hours.items():
        opens = info["opens_at"]
        closes = info["closes_at"]
        if opens and closes and opens <= now <= closes:
            open_now.append({
                "name": name,
                "opens_at": opens,
                "closes_at": closes
            })
    return open_now
