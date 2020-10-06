from bs4 import BeautifulSoup
import requests
import datefinder
import datetime
import json
import re

rki_site = "https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Risikogebiete_neu.html"

#convert german country names to iso codes
# https://stefangabos.github.io/world_countries/
def country2iso(json_object, name):
    for dict in json_object:
        if name in dict['name']:
            return dict['alpha3'].upper()

def scrape():
    # load json with countries
    with open('world.json') as f:
        world = json.load(f)

    # get website
    result = requests.get(rki_site)
    src = result.content
    soup = BeautifulSoup(src,features="html.parser")

    # just grab main div, skip navigation, and get the ul tag inside main tag
    main_list = soup.find("div", id='main').find("ul").contents

    countries = []
    regions = []

    for entry in main_list:
        # check for children tags to extract regions
        if len(list(entry.descendants)) > 1:
            children = list(entry.find("ul").contents)
            for x in children:
                if 'Ausnahme' in x.text:
                    print('Ausnahme!')
                regions.append(x.text)
        else:
            # country without regions
            # extract date from entry
            date = next(datefinder.find_dates(entry.text)).date()
            date = date.strftime('%d.%m.%Y')

            # split string on whitespace to get country without date
            country = re.split(r' \(| \–| \-',entry.text)[0]
            iso_country = country2iso(world,country)
            if not iso_country:
                print('No match for: '+ country)
            countries.append(iso_country)

    return countries

