__author__ = 'smcfall'

# simple script to mess with the bs4 library

from bs4 import BeautifulSoup
import requests


url = "www.wdfw.wa.gov/fishing/creel/steelhead/"

r = requests.get("http://" + url)

data = r.text

soup = BeautifulSoup(data)

# get table title


#get table cells
table1 = soup(bgcolor="#666666")[0]

for i in table1:
    # drop empty elements
    if len(i) > 1:
        date = i.contents[1].string
        anglers = i.contents[3].string

        print "{} {}".format(date,anglers)
