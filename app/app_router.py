from app.intent import classify_intent
from app.matchers import match_location, match_item
from app.scrapers.hours import scrape_hours
from app.scrapers.menu import scrape_menu
from app.scrapers.label import scrape_label_page
from app.llm import ask_llm

def route_request(user_message):
    from app.state import cached_hours
    print("DEBUG HOURS COUNT:", len(cached_hours.get("units", [])))
    intent = classify_intent(user_message)
    context = {}

    if intent == "OPEN_LOCATIONS":
        units = cached_hours.get("units",[])
        
        from app.state import cached_hours
        import json

        print(">>> CURRENT CACHED HOURS:")
        print(json.dumps(cached_hours, indent=2))

        
        #1. extract the time the user is asking about
        from app.time_utils import extract_requested_time, is_open_at
        requested_time = extract_requested_time(user_message)
        
        #2. filter units BEFORE sending to LLM
        open_units = [
            u for u in units
            if is_open_at(u, requested_time)
        ]
        
        #3. pass only filtered units to the LLM
        context["hours"] = open_units
        context["requested_time"] = requested_time.strftime("%H:%M")
        
        print("REQUESTED TIME:", requested_time)
        for u in units:
            print(u["name"], u["hours"])
        
    elif intent == "LOCATION_MENU":
        location = match_location(user_message)
        if not location:
            return "I couldn't identify a dining location."
        menu = scrape_menu(location["location_num"])
        context["menu"] = menu

    elif intent == "ITEM_DETAILS":
        item = match_item(user_message)
        if not item:
            return "I couldn't identify that food item."
        details = scrape_label_page(item["location_num"], item["recnum"])
        context["item_details"] = details

    elif intent == "DIET_FILTER":
        location = match_location(user_message)
        if not location:
            return "I couldn't identify a dining location."
        menu = scrape_menu(location["location_num"])
        context["menu"] = menu

    elif intent == "GENERAL_CHAT":
        context = {}

    return ask_llm(user_message, context)
