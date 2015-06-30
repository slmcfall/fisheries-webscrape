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
url = "www.wdfw.wa.gov/fishing/creel/steelhead/"
r = requests.get("http://" + url)
data = r.text
soup = BeautifulSoup(data)

riversDict = {"Bogachiel/Quillayute River": 0, "Calawah River": 1, "Sol Duc River": 2,
              "Lower Hoh River": 3, "Upper Hoh River": 4}

table_path = "C:\\Users\\Sean.McFall\\Documents\\SH\\fisheries-webscrape\\tables\\"
if not os.path.exists(table_path):
    os.makedirs(table_path)

for riverName, tableNum in riversDict.iteritems():

    table = soup(bgcolor="#666666")[tableNum]

    count = 0
    totals = len(table) - 2
    csvName = table_path + riverName[:3] + ".csv"

    with open(csvName, 'wb') as csvfile:
        csvOut = csv.writer(csvfile, delimiter=',')
        #csvOut.writerow(["River Name", "Date", "Num of Anglers", "WS Kept", "WS Rel",
                       #"HS Kept", "HS Rel", "Total Hours Fished", "Comments"])

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



                #csvOut.writerow([riverName,date,anglers,hrsPerFish,wsRel,hKept,hRel,hrs,comments])
                csvOut.writerow([riverName,date,anglers,hrsPerWS,wsCaught,hrsPerHS,hsCaught,wsKept,wsRel,hKept,hRel,hrs,comments])
                # probably want to add these to the bar graph output too, here
                # probably a list of lists would be suitable
            count += 1

    # convert csv to dbf
    dbf_table = dbf.from_csv(csvName, to_disk=True,
                            filename= table_path + riverName[:3],
                            field_names='RiverName Date NumOfAng hrsPerWS wsCaught hrsPerHS hsCaught wsKept wsRel hKept hRel HrsFished Comments'.split())

    arcpy.TableToTable_conversion(in_rows=table_path + riverName[:3] + '.csv', out_path="C:\\Users\\Sean.McFall\\Documents\\SH\\rivers.gdb",
                        out_name=riverName[:3])


#
# relate dbf to rivers layer
#

# arcpy.CreateRelationshipClass_management()
