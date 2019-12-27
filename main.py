from bs4 import BeautifulSoup
from requests import get
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
from datetime import date
sns.set()

headers = ({'User-Agent':
                'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})

# interesting_apartments = [
#     "https://www.voxcambridge.com/floorplans.aspx",
#     "https://www.hanoveralewife.com/cambridge/hanover-alewife/",
#     "https://www.livecambridgepark.com/floorplans",
#     "https://www.windsoratcambridgepark.com/floorplans.aspx",
#     "https://www.fusecambridge.com/floor-plans"]

apartment = "https://www.voxcambridge.com/floorplans.aspx"

def find_rent():
    rents = []
    r = get(apartment, headers=headers)
    soup = BeautifulSoup(r.content, "html5lib")

    for td in soup.find_all("td"):
        if td.get('data-label') == "Rent":
            if bool(re.search(r'\d',td.text)):
                #sorry future me. This removes commas from the Monthly Rent string and parses just the minimum rent number, puts it into an array
                rents.append(int(re.sub(',', '', td.text[13:18])))
    #returns daily rent prices in an array, no details about the room itself

    today = date.today().strftime('%Y-%m-%d')
    entry = str({today: sorted(rents)}) + "\n"
    return entry

def compare_rents(rents_array):
    desired_rent = 2650
    for rent in rents_array:
        if rent <= desired_rent:
            lowest_rent = min(rent, lowest_rent)
    message = "I found a rent lower than your desired rent at " + lowest_rent
    return message

def record_data(entry):
    with open("voxoncambridge.txt", "a") as data:
        data.write(entry)

record_data(find_rent())
