import numpy as np
import matplotlib.pyplot as plt
import csv

table_path = "C:\\Users\\Sean.McFall\\PycharmProjects\\fisheries-webscrape\\tables\\"

# read the csv
res = csv.reader(open(table_path + "Cal.csv"), delimiter = ',')
# skips the header
res.next()

date = []
SH = []
width = 0.2

for col in res:
    date.append(col[1])
    SH.append(int(col[2]))

#
# bar plot creation
#

tbl_ln = np.arange(len(date))

barplot = plt.bar(range(1,len(SH)+1),SH,width,color='r')
#labels = plt.xticks(SH,date, rotation='vertical')

plt.show()
