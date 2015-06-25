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
width = 0.8

for col in res:
    date.append(col[1])
    SH.append(int(col[2]))

#
# bar plot creation
#

tbl_ln = np.arange(len(date))
plt.figure(figsize=(15, 7))
barplot = plt.bar(range(1,len(SH)+1),SH,width,color='r',align='center')
labels = plt.xticks(range(1,len(SH)+1),date, rotation='vertical', ha='center')
plt.grid(True)


plt.show()
