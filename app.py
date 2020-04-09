from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import csv
import os
import pandas as pd
import time

# issue on Ne2


def pullData(postcode):

    url = "https://www.zoopla.co.uk/to-rent/property/" + postcode + \
        "?price_frequency=per_month&results_sort=newest_listings&search_source=to-rent&page_size=100"
    req = Request(url, headers={'User-Agent': "Magic Browser"})
    html = urlopen(req)
    soup = BeautifulSoup(html, features="html.parser")
    ads = soup.find_all(class_="listing-results-wrapper")
    data = []

    for ad in ads:
        details = ad.find(class_="listing-results-right")
        price = details.find("a").text
        # beds = details.find("h3").find("span")
        agent_img = ad.find(class_="agent_logo")
        if agent_img:
            agent = agent_img.find("img")
        else:
            agent = ''
        beds_confirm = details.find("h2").find("a").text
        description = ''
        descriptions = details.find_all("p")
        for item in descriptions:
            description = description + item.text.strip() + " "
        try:
            data.append([
                postcode,
                agent,
                price.strip(),
                # beds,
                beds_confirm.strip(),
                description.replace(',', '').encode("utf-8")
            ])
        except Exception:
            pass

    with open('data/' + postcode + '.csv', 'w', encoding='utf-8') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(data)
    csvFile.close()


# for file in os.scandir('data/'):
#     if file.name.endswith(".csv"):
#         os.unlink(file.path)

data = pd.read_csv('postcodes.csv', header=None)
postcodes = data[data.columns[0]]
count = 0
for postcode in postcodes:
    print(str(count) + ' of ' + str(len(postcodes)) + ' complete')
    time.sleep(1)
    pullData(postcode)
    count += 1
