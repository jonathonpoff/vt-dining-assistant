import requests
from bs4 import BeautifulSoup

def scrape_label_page(location_num, recnum):
    url = f"https://foodpro.students.vt.edu/menus/label.aspx?locationNum={location_num}&RecNumAndPort={recnum}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    data = {}

    # Calories
    cal_div = soup.find("div", id="calories_container")
    if cal_div:
        text = cal_div.get_text(strip=True)
        calories = ''.join(filter(str.isdigit, text))
        data["calories"] = calories

    # Nutrition facts
    nutrition = {}
    rows = soup.find_all("div", class_="col-lg-8 col-md-8 col-sm-8 col-xs-8")
    for row in rows:
        label_span = row.find("span", class_="fact_label")
        if not label_span:
            continue
        label = label_span.get_text(strip=True)
        full_text = row.get_text(" ", strip=True)
        value = full_text.replace(label, "").strip()
        nutrition[label] = value

    data["nutrition"] = nutrition

    # Ingredients
    ing_div = soup.find("div", class_="ingredients_container")
    if ing_div:
        full_text = ing_div.get_text(" ", strip=True)
        data["ingredients"] = full_text.replace("INGREDIENTS:", "").strip()

    # Allergens
    all_div = soup.find("div", class_="allergens_container")
    if all_div:
        full_text = all_div.get_text(" ", strip=True)
        cleaned = full_text.replace("ALLERGENS:", "").strip()
        allergens = [a.strip() for a in cleaned.replace(";", ",").split(",")]
        data["allergens"] = allergens

    return data