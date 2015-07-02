# bar graphs for washington fisheries data

import numpy as np
import csv
import os
import matplotlib.pyplot as plt

## paths
# windows
table_path = "C:\\Users\\Sean.McFall\\Documents\\SH\\fisheries-webscrape\\tables\\"
fig_path = "C:\\Users\\Sean.McFall\\Documents\\SH\\fisheries-webscrape\\figures\\"
# linux
#table_path = "/home/smcfall/Documents/fisheries-webscrape/tables/"
#fig_path = "/home/smcfall/Documents/fisheries-webscrape/figures/"

if not os.path.exists(fig_path):
    os.makedirs(fig_path)

tables = os.listdir(table_path)

def makeBar(position, data, x_labels, y_title, fill_color, line_bf):
    ax = fig.add_subplot(position)
    ax.bar(x_axis, data, width, color=fill_color, align='center')
    labels = plt.xticks(x_axis, x_labels, rotation='vertical', ha='center')
    plt.grid(True)
    ax.set_ylabel(y_title, fontweight='bold')
    plt.xlim([0,len(x_axis)+1])


    if line_bf == 1:

        # best fit of data
        (mu, sigma) = norm.fit(data)

        # the histogram of the data
        #bins = hist(datos, 60, normed=1, facecolor='green', alpha=0.75)

        # add a 'best fit' line
        deg = round(max(x_axis)/3)

        if deg % 2 == 0:
            deg += 1

        coefficients = np.polyfit(x_axis, data, deg)
        polynomial = np.poly1d(coefficients)
        xs = np.linspace(min(data), max(data), 1000)
        ys = polynomial(xs)

        plt.plot(xs,ys)

    axes = plt.gca()
    axes.set_ylim(min(data),max(data))

def createFig(table_name):
    global fig
    global x_axis
    global width
    #open csv

    # get list of csv files
    # iterate over list of files

    # read the csv
    res = csv.reader(open(table_path + table_name), delimiter = ',')

    # ang = anglers, ws = wild steelhead, h = hatchery steelhed, rel = released
    date, num_ang, hrsPerWS, wsCaught, hrsPerHS, hsCaught, hrs_fished = [], [], [], [], [], [], []

    # populate lists from csv
    for col in res:
        date.append(col[1])
        num_ang.append(int(col[2]))
        hrsPerWS.append(float(col[3]))
        wsCaught.append(int(col[4]))
        hrsPerHS.append(float(col[5]))
        hsCaught.append(int(col[6]))
        hrs_fished.append(float(col[11]))

        river_name = col[0]

    #
    # bar plot creation
    #

    width = 0.8
    x_axis = range(1,len(date)+1)
    bar_color = '#455A64'  # slate
    empty_list = ['']*len(date)

    # set size of the figure area

    fig = plt.figure(figsize=(15, 10))
    title = river_name + ' 2014/2015'
    title.upper()
    fig.suptitle(title.upper(), fontsize=16, fontweight='bold')
    # position, attributes, title

    # six plots
    num_ang_ax = makeBar(322,num_ang, empty_list,'Number of Anglers',bar_color,0)
    hrs_fished_ax = makeBar(321,hrs_fished,empty_list,'Hours Fished',bar_color,0)
    hrsPerWS_ax = makeBar(323,hrsPerWS,empty_list,'Hours Per \n Wild Steelhead','#FF5252',0)
    ws_caught_ax = makeBar(324,wsCaught,empty_list,'Wild Steelhead Caught','#FF5252',0)
    hrs_per_ws_ax = makeBar(325,hrsPerHS,date,'Hours Per \n Hatchery Steelhead','#8bc34a',0)
    hs_caught_ax = makeBar(326,hsCaught,date,'Hatchery Steelhead Caught','#8bc34a',0)

    # gives the x-axis labels enough room
    fig.tight_layout()
    plt.subplots_adjust(top=.92)
    #plt.savefig(fig_path + 'test.png', bbox_inches="tight")
    #plt.show()

    # save the figure
    plt.savefig(fig_path + table_name[:3], bbox_inches='tight')

for table in tables:
    if table[-3:] == 'csv':
        createFig(table)
