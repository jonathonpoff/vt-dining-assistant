from datetime import datetime, time
import re
import zoneinfo

# ----------------------------------------
# Parse the time the user is asking about
# ----------------------------------------

def extract_requested_time(message: str) -> time:
    """
    Returns a datetime.time object representing the time the user is asking about.
    Defaults to 'now' if no explicit time is found.
    """

    msg = message.lower()

    # 1. "now", "right now", "currently"
    if "now" in msg or "right now" in msg or "currently" in msg:
        eastern = zoneinfo.ZoneInfo("America/New_York")
        return datetime.now(eastern).time()

    # 2. Look for explicit times like "8pm", "8:30 pm", "20:00"
    match = re.search(r"(\d{1,2})(?::(\d{2}))?\s*(am|pm)?", msg)
    if match:
        hour = int(match.group(1))
        minute = int(match.group(2)) if match.group(2) else 0
        ampm = match.group(3)

        if ampm:
            if ampm == "pm" and hour != 12:
                hour += 12
            if ampm == "am" and hour == 12:
                hour = 0

        return time(hour, minute)

    # 3. Fallback → assume "now"
    eastern = zoneinfo.ZoneInfo("America/New_York")
    return datetime.now(eastern).time()


# ----------------------------------------
# Check if a unit is open at a given time
# ----------------------------------------

def is_open_at(unit: dict, t: time) -> bool:
    """
    Given a unit dict and a datetime.time, return True if the unit is open.
    """

    for block in unit.get("hours", []):
        try:
            open_t = datetime.strptime(block["open_time"], "%H:%M").time()
            close_t = datetime.strptime(block["close_time"], "%H:%M").time()
        except:
            continue

        # Normal same-day range
        if open_t <= t <= close_t:
            return True

        # Overnight range (e.g., 20:00 → 02:00)
        if open_t > close_t:
            if t >= open_t or t <= close_t:
                return True

    return False
