from app.intent import classify_intent
from app.matchers import match_location, match_item
from app.scrapers.hours import scrape_hours
from app.scrapers.menu import scrape_menu
from app.scrapers.label import scrape_label_page
from app.llm import ask_llm

def route_request(user_message):
    intent = classify_intent(user_message)
    context = {}

    if intent == "OPEN_LOCATIONS":
        hours = scrape_hours()
        context["hours"] = hours

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
