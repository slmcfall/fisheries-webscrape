__author__ = 'smcfall'

# simple script to mess with the bs4 library

from bs4 import BeautifulSoup
import requests


url = "www.wdfw.wa.gov/fishing/creel/steelhead/"

r = requests.get("http://" + url)

data = r.text

soup = BeautifulSoup(data)

# get table title

# get table cells
table1 = soup(bgcolor="#666666")[0]

count = 0
totals = len(table1) - 2

for i in table1:
    # drop empty elements
    if len(i) > 1 and count > 3 and count < totals:
        date = i.contents[1].string
        anglers = i.contents[3].string
        wsKept = i.contents[5].string

        print "{} {} {}".format(str(date), int(anglers), int(wsKept))

    count += 1
