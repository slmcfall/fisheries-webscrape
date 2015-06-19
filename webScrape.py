__author__ = 'smcfall'

# simple script to mess with the bs4 library

from bs4 import BeautifulSoup
import requests
import csv
import arcpy

arcpy.env.overwriteOutput = 1
arcpy.env.workspace = "in_memory"

url = "www.wdfw.wa.gov/fishing/creel/steelhead/"

r = requests.get("http://" + url)

data = r.text

soup = BeautifulSoup(data)

# get table title

# get table cells
table1 = soup(bgcolor="#666666")[0]

count = 0
totals = len(table1) - 2
riverName = "Bogachiel/Quillayute River"

with open('boga.csv', 'wb') as csvfile:
    boga = csv.writer(csvfile, delimiter=',')
    boga.writerow(["River Name", "Date", "Num of Anglers", "WS Kept", "WS Rel",
                   "HS Kept", "HS Rel", "Total Hours Fished", "Comments"])

    for i in table1:
        # drop empty elements
        if len(i) > 1 and count > 3 and count < totals:
            date = str(i.contents[1].string)
            anglers = int(i.contents[3].string)
            wsKept = int(i.contents[5].string)
            wsRel = int(i.contents[7].string)
            hKept = int(i.contents[9].string)
            hRel = int(i.contents[11].string)
            hrs = float(i.contents[13].string)
            comments = str(i.contents[15].string)

            print date
            boga.writerow([riverName,date,anglers,wsKept,wsRel,hKept,hRel,hrs,comments])
        count += 1

#
# convert csv to dbf
#

input_csv = "C:\\Users\\Sean.McFall\\PycharmProjects\\fisheries-webscrape\\boga.csv"
output_location = "C:\\Users\\Sean.McFall\\Documents\\SH"
output_name = "boga_txt.dbf"

arcpy.TableToTable_conversion(input_csv, output_location, output_name)