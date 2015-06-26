import numpy as np
import matplotlib.pyplot as plt
import csv

table_path = "C:\\Users\\Sean.McFall\\PycharmProjects\\fisheries-webscrape\\tables\\"
fig_path = "C:\\Users\\Sean.McFall\\PycharmProjects\\fisheries-webscrape\\figures\\"

# read the csv
res = csv.reader(open(table_path + "Cal.csv"), delimiter = ',')
# skips the header
res.next()

# ang = anglers, ws = wild steelhead, h = hatchery steelhed, rel = released
date, num_ang, ws_kept, ws_rel, h_kept, h_rel, hrs_fished = [], [], [], [], [], [], []

# populate lists from csv
for col in res:
    date.append(col[1])
    num_ang.append(int(col[2]))
    ws_kept.append(int(col[3]))
    ws_rel.append(int(col[4]))
    h_kept.append(int(col[5]))
    h_rel.append(int(col[6]))
    hrs_fished.append(float(col[7]))

#
# bar plot creation
#

width = 0.8
x_axis = range(1,len(date)+1)
bar_color = '#455A64'  # slate
empty_list = ['']*len(date)

# set size of the figure area
fig = plt.figure(figsize=(15, 10))
fig.suptitle('Calawah River 2014/2015', fontsize=14, fontweight='bold')
# position, attributes, title

def makeBar(position, data, x_labels, y_title):
    ax = fig.add_subplot(position)
    ax.bar(x_axis,data,width, color=bar_color, align='center')
    labels = plt.xticks(x_axis, x_labels, rotation='vertical', ha='center')
    plt.grid(True)
    ax.set_ylabel(y_title)
    plt.xlim([0,len(x_axis)+1])

# six plots
num_ang_ax = makeBar(321,num_ang, empty_list,'Number of Anglers')
hrs_fished_ax = makeBar(322,hrs_fished,empty_list,'Hours Fished')
ws_kept_ax = makeBar(323,ws_kept,empty_list,'Wild Steelhead Kept')
ws_rel_ax = makeBar(324,ws_rel,empty_list,'Wild Steelhead Released')
h_kept_ax = makeBar(325,h_kept,date,'Hatchery Steelhead Kept')
h_rel_ax = makeBar(326,h_rel,date,'Hatchery Steelhead Released')

# gives the x-axis labels enough room
fig.tight_layout()
plt.subplots_adjust(top=.92)
#plt.savefig(fig_path + 'test.png', bbox_inches="tight")
plt.show()
