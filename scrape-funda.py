import time
from bs4 import BeautifulSoup
import json
import requests
from alive_progress import alive_bar
from selenium import webdriver
import pandas as pd

driver = webdriver.Chrome()

csv_file = r"scrapped.csv"

room_list = []
wait_time = 1
start_time = time.time()


def parse(link):
    counter = 0

    while True:

        # loop through pages

        # collect html
        print("getting html...")
        driver.get(link)

        # if the page took long to fetch, then the CSR already took place
        print(f"giving {wait_time}s for CSR...")
        time.sleep(wait_time)

        # r = requests.get(f'{link}&start={counter}')
        r = requests.get(f"{link}")

        page_html = driver.page_source

        # print('page_html', page_html)

        room_data = BeautifulSoup(page_html, "lxml")

        print("parsing...")

        # picking up the data
        # try:
        cover_image = room_data.select_one(".object-media-fotos-container").get("src")
        title = room_data.select_one(
            "#content > div.object-detail.fd-container--xl.fd-m-auto > div > div.object-primary > header > div > div > div.object-header__details-info.fd-m-bottom-l.fd-m-bottom-s--bp-m.fd-flex > div.object-header__container.fd-m-right-xs.fd-flex-grow > h1 > span.object-header__title"
        ).text
        print("title", title)
        location = room_data.select_one(
            "#content > div.object-detail.fd-container--xl.fd-m-auto > div > div.object-primary > header > div > div > div.object-header__details-info.fd-m-bottom-l.fd-m-bottom-s--bp-m.fd-flex > div.object-header__container.fd-m-right-xs.fd-flex-grow > h1 > span.object-header__subtitle.fd-color-dark-3"
        ).text
        posted_by = room_data.select_one(
            "#content > div.object-detail.fd-container--xl.fd-m-auto > div > div.object-primary > header > div > div > div.object-header__details-info.fd-m-bottom-l.fd-m-bottom-s--bp-m.fd-flex > div.object-header__container.fd-m-right-xs.fd-flex-grow > h1 > span.object-header__subtitle.fd-color-dark-3 > a"
        ).text
        posted_by_url = room_data.select_one(
            "#content > div.object-detail.fd-container--xl.fd-m-auto > div > div.object-primary > header > div > div > div.object-header__details-info.fd-m-bottom-l.fd-m-bottom-s--bp-m.fd-flex > div.object-header__container.fd-m-right-xs.fd-flex-grow > h1 > span.object-header__subtitle.fd-color-dark-3 > a"
        ).get("href")
        floor_area = room_data.select_one(
            "#content > div.object-detail.fd-container--xl.fd-m-auto > div > div.object-primary > header > div > div > div.object-header__details-info.fd-m-bottom-l.fd-m-bottom-s--bp-m.fd-flex > div.object-header__container.fd-m-right-xs.fd-flex-grow > section > ul > li:nth-child(1) > span.kenmerken-highlighted__value.fd-text--nowrap"
        ).text
        wall_area = room_data.select_one(
            "#content > div.object-detail.fd-container--xl.fd-m-auto > div > div.object-primary > header > div > div > div.object-header__details-info.fd-m-bottom-l.fd-m-bottom-s--bp-m.fd-flex > div.object-header__container.fd-m-right-xs.fd-flex-grow > section > ul > li:nth-child(2) > span.kenmerken-highlighted__value.fd-text--nowrap"
        ).text
        room_number = room_data.select_one(
            "#content > div.object-detail.fd-container--xl.fd-m-auto > div > div.object-primary > header > div > div > div.object-header__details-info.fd-m-bottom-l.fd-m-bottom-s--bp-m.fd-flex > div.object-header__container.fd-m-right-xs.fd-flex-grow > section > ul > li:nth-child(3) > span.kenmerken-highlighted__value.fd-text--nowrap"
        ).text
        price = room_data.select_one(
            "#content > div.object-detail.fd-container--xl.fd-m-auto > div > div.object-primary > header > div > div > div.object-header__pricing.fd-text-size-l.fd-flex--bp-m.fd-align-items-center > div"
        ).text
        description = room_data.select_one("section.object-description > div").text
        print("description", description)
        asking_price = room_data.select_one(
            "#content > div.object-detail.fd-container--xl.fd-m-auto > div > div.object-primary > section.object-kenmerken.is-expandible.is-expanded > div > dl:nth-child(2) > dd:nth-child(2) > span.fd-m-right-xs"
        ).text
        offered_since = room_data.select_one(
            "#content > div.object-detail.fd-container--xl.fd-m-auto > div > div.object-primary > section.object-kenmerken.is-expandible.is-expanded > div > dl:nth-child(2) > dd:nth-child(6) > span"
        ).text
        status = room_data.select_one(
            "#content > div.object-detail.fd-container--xl.fd-m-auto > div > div.object-primary > section.object-kenmerken.is-expandible.is-expanded > div > dl:nth-child(2) > dd:nth-child(8) > span"
        ).text
        acceptance = room_data.select_one(
            "#content > div.object-detail.fd-container--xl.fd-m-auto > div > div.object-primary > section.object-kenmerken.is-expandible.is-expanded > div > dl:nth-child(2) > dd:nth-child(10)"
        ).text
        type_of_house = room_data.select_one(
            "#content > div.object-detail.fd-container--xl.fd-m-auto > div > div.object-primary > section.object-kenmerken.is-expandible.is-expanded > div > dl:nth-child(5) > dd:nth-child(2) > span"
        ).text
        type_of_construction = room_data.select_one(
            "#content > div.object-detail.fd-container--xl.fd-m-auto > div > div.object-primary > section.object-kenmerken.is-expandible.is-expanded > div > dl:nth-child(5) > dd:nth-child(4) > span"
        ).text
        construction_year = room_data.select_one(
            "#content > div.object-detail.fd-container--xl.fd-m-auto > div > div.object-primary > section.object-kenmerken.is-expandible.is-expanded > div > dl:nth-child(5) > dd:nth-child(6) > span.fd-m-right-xs"
        ).text
        type_of_roof = room_data.select_one(
            "#content > div.object-detail.fd-container--xl.fd-m-auto > div > div.object-primary > section.object-kenmerken.is-expandible.is-expanded > div > dl:nth-child(5) > dd:nth-child(8) > span"
        ).text
        living_space = room_data.select_one(
            "#content > div.object-detail.fd-container--xl.fd-m-auto > div > div.object-primary > section.object-kenmerken.is-expandible.is-expanded > div > dl:nth-child(8) > dd.object-kenmerken-group-list > dl > dd:nth-child(2) > span"
        ).text
        other_indoor_space = room_data.select_one(
            "#content > div.object-detail.fd-container--xl.fd-m-auto > div > div.object-primary > section.object-kenmerken.is-expandible.is-expanded > div > dl:nth-child(8) > dd.object-kenmerken-group-list > dl > dd:nth-child(4) > span"
        ).text
        plot = room_data.select_one(
            "#content > div.object-detail.fd-container--xl.fd-m-auto > div > div.object-primary > section.object-kenmerken.is-expandible.is-expanded > div > dl:nth-child(8) > dd:nth-child(5) > span"
        ).text
        contents = room_data.select_one(
            "#content > div.object-detail.fd-container--xl.fd-m-auto > div > div.object-primary > section.object-kenmerken.is-expandible.is-expanded > div > dl:nth-child(8) > dd:nth-child(7) > span"
        ).text
        number_of_rooms = room_data.select_one(
            "#content > div.object-detail.fd-container--xl.fd-m-auto > div > div.object-primary > section.object-kenmerken.is-expandible.is-expanded > div > dl:nth-child(11) > dd:nth-child(2) > span"
        ).text
        number_of_bathrooms = room_data.select_one(
            "#content > div.object-detail.fd-container--xl.fd-m-auto > div > div.object-primary > section.object-kenmerken.is-expandible.is-expanded > div > dl:nth-child(11) > dd:nth-child(4) > span"
        ).text
        bathroom_amenities = room_data.select_one(
            "#content > div.object-detail.fd-container--xl.fd-m-auto > div > div.object-primary > section.object-kenmerken.is-expandible.is-expanded > div > dl:nth-child(11) > dd:nth-child(6) > span"
        ).text
        number_of_floors = room_data.select_one(
            "#content > div.object-detail.fd-container--xl.fd-m-auto > div > div.object-primary > section.object-kenmerken.is-expandible.is-expanded > div > dl:nth-child(11) > dd:nth-child(8) > span"
        ).text
        services = room_data.select_one(
            "#content > div.object-detail.fd-container--xl.fd-m-auto > div > div.object-primary > section.object-kenmerken.is-expandible.is-expanded > div > dl:nth-child(11) > dd:nth-child(10) > span"
        ).text
        energy_label = room_data.select_one(
            "#content > div.object-detail.fd-container--xl.fd-m-auto > div > div.object-primary > section.object-kenmerken.is-expandible.is-expanded > div > dl:nth-child(14) > dd:nth-child(2) > span"
        ).text
        insulation = room_data.select_one(
            "#content > div.object-detail.fd-container--xl.fd-m-auto > div > div.object-primary > section.object-kenmerken.is-expandible.is-expanded > div > dl:nth-child(14) > dd:nth-child(4) > span"
        ).text
        heating = room_data.select_one(
            "#content > div.object-detail.fd-container--xl.fd-m-auto > div > div.object-primary > section.object-kenmerken.is-expandible.is-expanded > div > dl:nth-child(14) > dd:nth-child(6) > span"
        ).text
        hot_water = room_data.select_one(
            "#content > div.object-detail.fd-container--xl.fd-m-auto > div > div.object-primary > section.object-kenmerken.is-expandible.is-expanded > div > dl:nth-child(14) > dd:nth-child(8) > span"
        ).text
        boiler = room_data.select_one(
            "#content > div.object-detail.fd-container--xl.fd-m-auto > div > div.object-primary > section.object-kenmerken.is-expandible.is-expanded > div > dl:nth-child(14) > dd:nth-child(10) > span"
        ).text
        cadastral_map_url = room_data.select_one(
            "#content > div.object-detail.fd-container--xl.fd-m-auto > div > div.object-primary > section.object-kenmerken.is-expandible.is-expanded > div > dl:nth-child(17) > dd:nth-child(2) > a"
        ).get("href")
        cadastral_surface = room_data.select_one(
            "#content > div.object-detail.fd-container--xl.fd-m-auto > div > div.object-primary > section.object-kenmerken.is-expandible.is-expanded > div > dl:nth-child(17) > dd.object-kenmerken-group-list > dl > dd:nth-child(2) > span"
        ).text
        cadastral_ownership_situation = room_data.select_one(
            "#content > div.object-detail.fd-container--xl.fd-m-auto > div > div.object-primary > section.object-kenmerken.is-expandible.is-expanded > div > dl:nth-child(17) > dd.object-kenmerken-group-list > dl > dd:nth-child(4) > span"
        ).text
        outdoor_location = room_data.select_one(
            "#content > div.object-detail.fd-container--xl.fd-m-auto > div > div.object-primary > section.object-kenmerken.is-expandible.is-expanded > div > dl:nth-child(19) > dd:nth-child(2) > span"
        ).text
        outdoor_garden = room_data.select_one(
            "#content > div.object-detail.fd-container--xl.fd-m-auto > div > div.object-primary > section.object-kenmerken.is-expandible.is-expanded > div > dl:nth-child(19) > dd:nth-child(4) > span"
        ).text
        outdoor_backyard = room_data.select_one(
            "#content > div.object-detail.fd-container--xl.fd-m-auto > div > div.object-primary > section.object-kenmerken.is-expandible.is-expanded > div > dl:nth-child(19) > dd:nth-child(6) > span"
        ).text
        outdoor_garden_location = room_data.select_one(
            "#content > div.object-detail.fd-container--xl.fd-m-auto > div > div.object-primary > section.object-kenmerken.is-expandible.is-expanded > div > dl:nth-child(19) > dd:nth-child(8) > span"
        ).text
        type_of_parking = room_data.select_one(
            "#content > div.object-detail.fd-container--xl.fd-m-auto > div > div.object-primary > section.object-kenmerken.is-expandible.is-expanded > div > dl:nth-child(22) > dd > span"
        ).text

        room_list.append(
            {
                "url": link,
                "cover_image": cover_image,
                "title": title.strip(),
                "location": location.strip(),
                "posted_by": posted_by.strip(),
                "posted_by_url": posted_by_url,
                "floor_area": floor_area.strip(),
                "wall_area": wall_area.strip(),
                "room_number": room_number.strip(),
                "price": price.strip(),
                "description": description.strip(),
                "asking_price": asking_price.strip(),
                "offered_since": offered_since.strip(),
                "status": status.strip(),
                "acceptance": acceptance.strip(),
                "type_of_house": type_of_house.strip(),
                "type_of_construction": type_of_construction.strip(),
                "construction_year": construction_year.strip(),
                "type_of_roof": type_of_roof.strip(),
                "living_space": living_space.strip(),
                "other_indoor_space": other_indoor_space.strip(),
                "plot": plot.strip(),
                "contents": contents.strip(),
                "number_of_rooms": number_of_rooms.strip(),
                "number_of_bathrooms": number_of_bathrooms.strip(),
                "bathroom_amenities": bathroom_amenities.strip(),
                "number_of_floors": number_of_floors.strip(),
                "services": services.strip(),
                "insulation": insulation.strip(),
                "heating": heating.strip(),
                "hot_water": hot_water.strip(),
                "boiler": boiler.strip(),
                "cadastral_map_url": cadastral_map_url,
                "cadastral_surface": cadastral_surface.strip(),
                "cadastral_ownership_situation": cadastral_ownership_situation.strip(),
                "energy_label": energy_label.strip(),
                "outdoor_location": outdoor_location.strip(),
                "outdoor_garden": outdoor_garden.strip(),
                "outdoor_backyard": outdoor_backyard.strip(),
                "outdoor_garden_location": outdoor_garden_location.strip(),
                "type_of_parking": type_of_parking.strip(),
            }
        )
        # finally:
        #   continue

        counter += 1
        yield
        break


def getLinks():

    counter = 0

    while True:

        rooms_selector = "a.top-position-object-link, div.search-result-media > a"

        # loop through pages

        # collect html
        print("getting html...")

        r = requests.get(f"{link}&start={counter}")

        soup = BeautifulSoup(r.text, "lxml")

        # print('html', soup)

        print("parsing...")

        rooms_selected = soup.select(rooms_selector)

        if len(rooms_selected) < 0:
            print(f"less than {0} rooms found in {link}. Finishing up.")
            break

        for room in rooms_selected:
            # picking up the data
            try:
                title = room.select_one(".pull-left > h4").text
                by = room.select_one(".pull-left > span > a.username").text
                meta_section_1 = room.select_one(".pull-left > span").text
                content = room.select_one("div.content").text
                url = room.select_one(".clearfix > .pull-right > a").get("href")

                room_list.append(
                    {
                        "title": title.strip(),
                        "by": by.strip(),
                        "content": content.strip(),
                        "time": meta_section_1.split("¦")[1].replace("\xa0", ""),
                        "url": url.strip(),
                    }
                )
            finally:
                continue

        counter += 1
        yield


# getting links
# print('getting links..')
# link_list = getLinks()
# saving them
link_list = [
    "https://www.funda.nl/koop/heel-nederland/p5/",
]

# looping through pages
print("")
for link in link_list:
    print(f"fetching rooms... >> {link} \n")
    with alive_bar(0) as bar:
        for i in parse(
            "https://www.funda.nl/koop/altforst/huis-88080129-het-gangske-3/"
        ):
            time.sleep(0.001)
            bar()

        # creating csv file
        df = pd.DataFrame(room_list)
        print("creating csv file...")
        df.to_csv(csv_file, index=None)


print("\n")
print(len(room_list), f"rooms collected. saved in {csv_file}")
