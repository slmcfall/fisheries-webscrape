__author__ = 'smcfall'

# simple script to mess with the bs4 library

from bs4 import BeautifulSoup
import requests

url = "www.wdfw.wa.gov/fishing/creel/steelhead/"

r = requests.get("http://" + url)

data = r.text

soup = BeautifulSoup(data)

# tables = list()
# for incident in soup('table'):
#     tables.append(incident)

#print tables[0].tr

#print soup.findAll(bgcolor="#666666")[1]

print soup(bgcolor = "#666666")

#for i in soup.table.contents[3]:
    #print i

#for i in soup.findAll("table", {"class" : "reading_text"})[2].tr:
#    print type(i)