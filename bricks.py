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

print("Enter Rig Number: ") 
rignum = input() 
print("Enter Start Date (YYYYMMDD): ") 
start = input() 
print("Enter End Date (YYYYMMDD): ") 
end = input() 

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

connection = sql.connect(
                        server_hostname = "adb-6462168382859837.17.azuredatabricks.net",
                        http_path = "/sql/1.0/warehouses/e4b92a848b76d8d8",
                        access_token = "dapi8a2bcdcce03f032880b581750a948d39-2")

cursor = connection.cursor()

query = '''SELECT ''' + tags + ''' FROM delta.osd
        WHERE rignumber = ''' + rignum + '''
        AND bottomdepth > 1
        AND bottomdepth - bitdepth < 1/10
        AND ad_on = 1
        AND daypartition BETWEEN ''' + start + ''' AND ''' + end + ''';'''

cursor.execute(query)

c = cursor.fetchall()
fp = open('file.csv', 'w')
myFile = csv.writer(fp)
myFile.writerow(header)
myFile.writerows(c)
fp.close()

df = pd.read_csv('file.csv') 
print("Graphing " + 'file.csv' + ".....") 

fig, ax = plt.subplots()
ax2 = ax.twinx()
#fig2 = plt.figure(2)

#font dictionary
font = {'family': 'monospace',
        'color':  'black',
        'weight': 'normal',
        'size': 16,
        }

#size and dpi of graph
plt.rcParams['figure.figsize'] = (5, 3)
plt.rcParams['figure.dpi'] = 75

#size of labels
plt.rc('xtick', labelsize=18)    
plt.rc('ytick', labelsize=18)    
plt.rc('legend', fontsize=12) 

data = df.sort_values(by=['riglocaltime'], ignore_index = True)

x = data.riglocaltime
x = np.asanyarray(x, dtype = 'datetime64[s]')

y1 = data.adpvdeltap
y2 = data.adspdeltap
y3 = data.adpvrop
y4 = data.adsprop
y5 = data.adpvwob
y6 = data.adspwob
y7 = data.topdrivetorque
y8 = data.topdrivespeed
y9 = data.tdoscltoffset
y10 = data.tdoscltspdsp
y11 = data.tdoscltfwdpossp
y12 = data.tdoscltrevrossp
y13 = data.tdosclttrqlim
y14 = data.tdcontrqsp
y15 = data.bitdepth
y16 = data.bottomdepth
y17 = data.standpipepressure
y18 = data.hookload
y19 = data.tdmodestate

# PLOT DATA #
l1, = ax2.plot(x, y1, 'maroon', label='adpvdeltap')
l2, = ax2.plot(x, y2,'red', label='adspdeltap')
l3, = ax.plot(x, y3, 'darkorange', label='adpvrop')
l4, = ax.plot(x, y4, 'gold', label='adsprop')
l5, = ax.plot(x, y5, 'yellowgreen', label='adpvwob')
l6, = ax.plot(x, y6, 'lawngreen', label='adspwob')
l7, = ax.plot(x, y7, 'forestgreen', label='topdrivetorque')
l8, = ax.plot(x, y8, 'lightseagreen', label='topdrivespeed')
l9, = ax.plot(x, y9, 'darkcyan', label='tdoscltoffset')
l10, = ax.plot(x, y10, 'dodgerblue', label='tdoscltspdsp')
l11, = ax.plot(x, y11, 'steelblue', label='tdoscltfwdpossp')
l12, = ax.plot(x, y12, 'navy', label='tdoscltrevpossp')
l13, = ax.plot(x, y13, 'blue', label='tdpsclttrqlim')
l14, = ax.plot(x, y14, 'blueviolet', label='tdcontrqsp')
l15, = ax2.plot(x, y15, 'magenta', label='bitdepth')
l16, = ax2.plot(x, y16, 'mediumvioletred', label='bottomdepth')
l17, = ax2.plot(x, y17, 'hotpink', label='standpipepressure')
l18, = ax.plot(x, y18, 'purple', label='hookload')

#l19, = plt.step(x, y19, 'black', label='tdmodestate') #seperate window

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
ax.legend(bbox_to_anchor=(-0.05, 1), loc='upper right', borderaxespad=0)
ax2.legend(bbox_to_anchor=(1.005, 1), loc='upper left', borderaxespad=0)
#tdmodestate legend
#fig2.legend()

#title is name of the file
ax.set_title('data')

cursor.close()

#annotated cursor - displays data at a single point when hovered over
cursor = mplcursors.cursor(hover=True)
#prompts matplotlib to open (displays your graph)
plt.show()

#ends the program when x button clicked in matplotlib graph
print("Graph closed. :)")

connection.close()
exit()

