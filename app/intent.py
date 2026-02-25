def classify_intent(message):
    msg = message.lower()

    if any(word in msg for word in ["open", "hours", "close"]):
        return "OPEN_LOCATIONS"

    if any(loc in msg for loc in ["west end", "turner", "owens", "hokie grill"]):
        return "LOCATION_MENU"

    if any(word in msg for word in ["calories", "nutrition", "ingredients", "allergens"]):
        return "ITEM_DETAILS"

    if any(word in msg for word in ["vegan", "vegetarian", "gluten", "protein", "healthy"]):
        return "DIET_FILTER"

    return "GENERAL_CHAT"