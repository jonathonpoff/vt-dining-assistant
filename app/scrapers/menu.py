import requests
from bs4 import BeautifulSoup

def scrape_menu(location_num):
    url = f"https://foodpro.students.vt.edu/menus/MenuAtLocation.aspx?locationNum={location_num}&naFlag=1"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    menu = {"location_num": location_num, "stations": []}

    station_headers = soup.find_all("h2", class_="station")
    for header in station_headers:
        station_name = header.get_text(strip=True)
        items = []

        ul = header.find_next("ul")
        if not ul:
            continue

        for li in ul.find_all("li"):
            a = li.find("a")
            if not a:
                continue

            name = a.get_text(strip=True)
            href = a.get("href")
            recnum = href.split("RecNumAndPort=")[-1]

            items.append({
                "name": name,
                "recnum": recnum,
                "location_num": location_num
            })

        menu["stations"].append({
            "station_name": station_name,
            "items": items
        })

    return menu