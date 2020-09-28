# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 08:11:38 2020

@author: Naomi
"""

import csv
import random
import requests
import selenium

from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options

# from requests_html import HTMLSession
# import pandas as pandas
sleepTimes = [2.1, 2.8, 3.2, 4, 5.2]
larger_sleep_times = [10, 12, 15]
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Dnt": "1",
    "Host": "httpbin.org",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
}
# url = "https://www.realo.be/en"
url = "https://www.realo.be/en/search/house,flat/for-sale?savedSearchId=18538987&saved=1"

file = open("listings.csv", "w")
writer = csv.writer(file, delimiter=",", quotechar='"')
print("Open file for writting")


def fetch_listings(url, page):
    # scrape the page using beautiful soup
    property_links = []
    if page > 1:
        url = f"https://www.realo.be/en/search/house,flat/for-sale?page={page}"

    print(url)
    print("Fetching search results")
    results = requests.get(url).text
    soup = BeautifulSoup(results, "html.parser")
    lists = soup.find_all("div", class_="body")

    for lst in lists:
        try:
            link = lst.find("a", class_="link")["href"].strip()
            property_links.append("https://www.realo.be" + link)
        except Exception:
            pass
    garden = "No"
    garage = "No"
    terrace = "No"
    furnished = "No"
    swimming_pool = "No"
    equipped_kitchen = "No"
    state_of_building = "No"
    open_fire = "No"
    property_type = ""
    heating = ""
    bathrooms = 0
    number_of_rooms = 0
    area = 0
    land_surface_area = 0

    for each_property in property_links:
        print("Fetching listing")
        sleep(random.choice(larger_sleep_times))
        property = requests.get(each_property).text
        soup = BeautifulSoup(property, "html.parser")

        try:
            address = soup.find("h1", class_="address").get_text().strip()
        except Exception:
            address = ""

        try:
            price = soup.find("div", class_="value").text
        except Exception:
            price = 0

        try:
            tags_li = soup.find("div", class_="component-property-description__tags").find_all("li")
        except Exception:
            tags_li = None

        if tags_li:
            for tg in tags_li:
                tag = tg.text.strip()

                if tag == "Garden":
                    garden = "Yes"
                if tag == "Garage":
                    garage = "Yes"
                if tag == "Terrace":
                    terrace = "Yes"
                if tag == "Swimming Pool":
                    swimming_pool = "Yes"
                if tag == "Equipped Kitchen":
                    equipped_kitchen = "Yes"
                if tag == "Furnished":
                    furnished = "Yes"
                if tag == "New Build":
                    state_of_building = "Yes"

        feature_table = soup.find("div", class_="component-property-features").find("table")
        trs = feature_table.find_all("tr")
        for tr in trs:
            tds = tr.find_all("td")
            name = tds[0].get_text()
            value = tds[1].get_text().strip()

            if name == "Property type":
                property_type = value
            elif name == "Bathrooms":
                bathrooms = value
            elif name == "Bedrooms":
                number_of_rooms = value
            elif name == "Habitable area":
                area = value
            elif name == "Lot size":
                land_surface_area = value
            elif name == "Heating type":
                heating = value

        print("Writting to file")
        writer.writerow(
            [
                address,
                price,
                property_type,
                number_of_rooms,
                area,
                equipped_kitchen,
                furnished,
                garage,
                open_fire,
                terrace,
                garden,
                swimming_pool,
                state_of_building,
                each_property,
            ]
        )
        file.flush()

    page += 1
    next_page_url = f"https://www.realo.be/en/search/house,flat/for-sale?page={page}"
    sleep(15)
    print(f"Fetching next page - {page} results")
    fetch_listings(next_page_url, page)


# write title row
writer.writerow(
    [
        "Locality",
        "Price",
        "Property type",
        "Number of rooms",
        "Area",
        "Equipped kitchen",
        "Furnished",
        "Garage" "open_fire",
        "Terrace",
        "Garden",
        "Swimming pool",
        "New building",
        "Link",
    ]
)

fetch_listings(url, 3)
file.close()