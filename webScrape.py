# webscrapes washington state fisheries data and outputs csv and dbfs of them

from bs4 import BeautifulSoup
import requests
import csv
import dbf
import os
import arcpy

# set arcgis parameters
arcpy.env.overwriteOutput = 1
arcpy.env.workspace = "in_memory"

# pull down html, make into soup object
print "--- Pulling down the data..."
url = "www.wdfw.wa.gov/fishing/creel/steelhead/"
r = requests.get("http://" + url)
data = r.text
soup = BeautifulSoup(data)

riversDict = {"Bogachiel/Quillayute River": 0, "Calawah River": 1, "Sol Duc River": 2,
              "Lower Hoh River": 3, "Upper Hoh River": 4}

gdb_path = "C:\\Users\\Sean.McFall\\Documents\\SH\\rivers.gdb"
table_path = "C:\\Users\\Sean.McFall\\Documents\\SH\\fisheries-webscrape\\tables\\"

# make table path if it doesn't exist already
if not os.path.exists(table_path):
    os.makedirs(table_path)

print "--- Creating tables..."
for riverName, tableNum in riversDict.iteritems():

    table = soup(bgcolor="#666666")[tableNum]

    count = 0
    totals = len(table) - 2
    csvName = table_path + riverName[:3] + ".csv"

    with open(csvName, 'wb') as csvfile:
        csvOut = csv.writer(csvfile, delimiter=',')
        csvOut.writerow(["River Name", "Date", "NumAnglers", "HrsPerWS", "wsCaught",
                       "HrsPerHS", "hsCaught", "wsKept", "wsRel","hKept","hRel", "HrsFished", "Comments"])

        for i in table:
            # drop empty elements
            if len(i) > 1 and count > 3 and count < totals:

                date     = str(i.contents[1].string)
                anglers  = int(i.contents[3].string)
                hrs      = float(i.contents[13].string)
                comments = str(i.contents[15].string)

                # wild steelhead calculations
                wsKept   = int(i.contents[5].string)
                wsRel    = int(i.contents[7].string)
                wsCaught = wsKept + wsRel
                if hrs == 0 or wsCaught == 0:
                    hrsPerWS = 0
                else:
                    hrsPerWS = hrs / float(wsCaught)

                # hatchery steelhead calculations
                hKept    = int(i.contents[9].string)
                hRel     = int(i.contents[11].string)
                hsCaught = hKept + hRel
                if hrs == 0 or hsCaught == 0:
                    hrsPerHS = 0
                else:
                    hrsPerHS = hrs / float(hsCaught)

                # write data to csv
                csvOut.writerow([riverName,date,anglers,hrsPerWS,wsCaught,hrsPerHS,hsCaught,wsKept,wsRel,hKept,hRel,hrs,comments])

            count += 1

# combine all csv's into one dbf
print "--- Combining tables..."
tables = os.listdir(table_path)

waAll = table_path + 'WA_SH.csv'
header = "RiverName,Date,NumAnglers,HrsPerWS,wsCaught,HrsPerHS,hsCaught,wsKept,wsRel,hKept,hRel,HrsFished,Comments\n"

with open(waAll, 'wb') as csvAll:
    csvAll.write(header)
    for table in tables:
        if table[-3:] == 'csv' and table != 'WA_SH.csv':
            header = 0
            for line in open(table_path + table):
                if header != 0:
                    csvAll.write(line)
                else:
                    header = 1

print "--- Exporting to dbf..."
# import csv into gdb
arcpy.TableToTable_conversion(in_rows=table_path + 'WA_SH.csv', out_path=gdb_path,
                    out_name='WA_SH')

# relate dbf to rivers layer
# arcpy.CreateRelationshipClass_management()
