#############################################
# Date: 07/24/23
# Author: Alekhyaa
# Description: Pull tags from Databricks.
#############################################

#import libraries
from databricks import sql
import os
import csv
from time import localtime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import mplcursors
from matplotlib.widgets import CheckButtons

#grab input from user - in terminal
print("Enter Rig Number: ") 
rignum = input() 
print("Enter Start Date (YYYYMMDD): ") 
start = input() 
print("Enter End Date (YYYYMMDD): ") 
end = input() 
print("What would you like to name your file? \n(include file extension)")
fileName = input() 
print("Gathering info for Rig " + rignum + ".....")

# tags to be pulled - add or delete
header = ['riglocaltime', 
          'adpvwob', 
          'adpvrop', 
          'adsprop', 
          'adpvdeltap', 
          'adspdeltap', 
          'adpvtorque',          
          'adsptorque',
          'adspwob',
          'tdmodestate',
          'topdrivespeed',
          'topdrivetorque',
          'blockvelocity',
          'elevatorposition',
          'hookload',
          'standpipepressure',
          'bitdepth',
          'bottomdepth',
          'utctimeseconds',
          'mp3vfdfreqpv',
          'mp2vfdfreqpv',
          'mp1vfdfreqpv',
          'pump1strokes',
          'pump2strokes',
          'pump3strokes',
          'mplinersizesp',
          'tdvfdrevst',
          'tdmtrenccnts',
          'tdoscltrevrossp',
          'tdoscltfwdpossp',
          'tdoscltoffset',
          'tdoscltspdsp',
          'tdosclttrqlim',
          'tdcontrqsp']

tags = ", ".join(header)

#establish databricks connection to SQL warehouse
connection = sql.connect(
                        server_hostname = "adb-6462168382859837.17.azuredatabricks.net",
                        http_path = "/sql/1.0/warehouses/e4b92a848b76d8d8",
                        access_token = "dapi8a2bcdcce03f032880b581750a948d39-2")
cursor = connection.cursor()

#SQL query
query = '''SELECT ''' + tags + ''' FROM delta.osd
        WHERE rignumber = ''' + rignum + '''
        AND bottomdepth > 1
        AND bottomdepth - bitdepth < 1/10
        AND ad_on = 1
        AND daypartition BETWEEN ''' + start + ''' AND ''' + end + ''';'''
cursor.execute(query)

#write data to csv
c = cursor.fetchall()
fp = open(fileName, 'w')
myFile = csv.writer(fp)
myFile.writerow(header)
myFile.writerows(c)
fp.close()

#read the csv file
df = pd.read_csv(fileName) 
print("Graphing " + fileName + ".....") 

#figures
fig, ax = plt.subplots()
ax2 = ax.twinx()
#fig2 = plt.figure(2)

#font dictionary
font = {
        'color':  'black',
        'weight': 'bold',
        'size': 16,
        }

#size and dpi of graph
plt.rcParams['figure.figsize'] = (5, 3)
plt.rcParams['figure.dpi'] = 75

#size of labels
plt.rc('xtick', labelsize=18)    
plt.rc('ytick', labelsize=18)    
plt.rc('legend', fontsize=12) 

#sort the data by time
data = df.sort_values(by=['riglocaltime'], ignore_index = True)
x = data.riglocaltime
x = np.asanyarray(x, dtype = 'datetime64[s]')

# PLOT DATA #
l1, = ax2.plot(x, data.adpvdeltap, 'maroon', label='adpvdeltap')
l2, = ax2.plot(x, data.adspdeltap,'red', label='adspdeltap')
l3, = ax.plot(x, data.adpvrop, 'darkorange', label='adpvrop')
l4, = ax.plot(x, data.adsprop, 'gold', label='adsprop')
l5, = ax.plot(x, data.adpvwob, 'yellowgreen', label='adpvwob')
l6, = ax.plot(x, data.adspwob, 'lawngreen', label='adspwob')
l7, = ax.plot(x, data.topdrivetorque, 'forestgreen', label='topdrivetorque')
l8, = ax.plot(x, data.topdrivespeed, 'lightseagreen', label='topdrivespeed')
l9, = ax.plot(x, data.tdoscltoffset, 'darkcyan', label='tdoscltoffset')
l10, = ax.plot(x, data.tdoscltspdsp, 'dodgerblue', label='tdoscltspdsp')
l11, = ax.plot(x, data.tdoscltfwdpossp, 'steelblue', label='tdoscltfwdpossp')
l12, = ax.plot(x, data.tdoscltrevrossp, 'navy', label='tdoscltrevpossp')
l13, = ax.plot(x, data.tdosclttrqlim, 'blue', label='tdpsclttrqlim')
l14, = ax.plot(x, data.tdcontrqsp, 'blueviolet', label='tdcontrqsp')
l15, = ax2.plot(x, data.bitdepth, 'magenta', label='bitdepth')
l16, = ax2.plot(x, data.bottomdepth, 'mediumvioletred', label='bottomdepth')
l17, = ax2.plot(x, data.standpipepressure, 'hotpink', label='standpipepressure')
l18, = ax.plot(x, data.hookload, 'purple', label='hookload')

#l19, = plt.step(x, data.tdmodestate, 'black', label='tdmodestate') #seperate window

#grab colors for check buttons
lines_by_label = {l.get_label(): l for l in [l1, l2, l3, l4, l5 ,l6, l7, l8, l9, l10, l11, l12, l13, l14, l15, l16, l17, l18]}
line_colors = [l.get_color() for l in lines_by_label.values()]

# Make checkbuttons with all plotted lines with correct visibility
rax = fig.add_axes([0.008, 0.09, 0.1, 0.3])
check = CheckButtons(
    ax=rax,
    labels=lines_by_label.keys(),
    actives=[l.get_visible() for l in lines_by_label.values()],
    label_props={'color': line_colors},
    frame_props={'edgecolor': line_colors},
    check_props={'facecolor': line_colors},
)

# callback for checkbuttons
def callback(label):
    ln = lines_by_label[label]
    ln.set_visible(not ln.get_visible())
    ln.figure.canvas.draw_idle()
#check if clicked
check.on_clicked(callback)

#creates a grid behind lines
ax.grid()

#legend corresponding to each scale
ax.legend(bbox_to_anchor=(-0.05, 1), fontsize = '12', loc='upper right', borderaxespad=0)
ax2.legend(bbox_to_anchor=(1.005, 1), fontsize = '12', loc='upper left', borderaxespad=0)
#tdmodestate legend
#fig2.legend()

#title is name of the file
ax.set_title('Rig ' + rignum + ' from ' + start + ' to ' + end, fontdict=font)
cursor.close()

#annotated cursor - displays data at a single point when hovered over
cursor = mplcursors.cursor(hover=True)

#rewrite csv file with sorted data
data.to_csv(fileName, index=False)

#prompts matplotlib to open (displays your graph)
plt.show()

#ends the program when x button clicked in matplotlib graph
print("Graph closed. :)")

#end connection
connection.close()

#end program
exit()

