__author__ = 'smcfall'

# simple script to mess with the bs4 library

from bs4 import BeautifulSoup
import requests
import csv
import dbf
#import arcpy

# set arcgis parameters
#arcpy.env.overwriteOutput = 1
#arcpy.env.workspace = "in_memory"

# pull down html, make into soup object
url = "www.wdfw.wa.gov/fishing/creel/steelhead/"
r = requests.get("http://" + url)
data = r.text
soup = BeautifulSoup(data)

riversDict = {"Bogachiel/Quillayute River": 0, "Calawah River": 1, "Sol Duc River": 2,
              "Lower Hoh River": 3, "Upper Hoh River": 4}

# get table cells

for riverName, tableNum in riversDict.iteritems():

    table = soup(bgcolor="#666666")[tableNum]

    count = 0
    totals = len(table) - 2
    csvName = riverName[:3] + ".csv"

    with open(csvName, 'wb') as csvfile:
        csvOut = csv.writer(csvfile, delimiter=',')
        #csvOut.writerow(["River Name", "Date", "Num of Anglers", "WS Kept", "WS Rel",
                       #"HS Kept", "HS Rel", "Total Hours Fished", "Comments"])

        for i in table:
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

                csvOut.writerow([riverName,date,anglers,wsKept,wsRel,hKept,hRel,hrs,comments])
            count += 1

#
# convert csv to dbf
#

# 1. arcpy method

# input_csv = "C:\\Users\\Sean.McFall\\PycharmProjects\\fisheries-webscrape\\boga.csv"
# output_location = "C:\\Users\\Sean.McFall\\Documents\\SH"
# output_name = "boga_txt.dbf"
#
# arcpy.TableToTable_conversion(input_csv, output_location, output_name)

# 2. pythonic method

dbf_table = dbf.from_csv('Cal.csv', to_disk=True, filename='CalNoHeaders', 
    field_names='RiverName Date NumOfAng wsKept wsRel hsKept hsRel HrsFished Comments'.split())
#dbf_table[0].delete_record()
print dbf_table
#
#

#
# relate dbf to rivers layer
#

# arcpy.CreateRelationshipClass_management()