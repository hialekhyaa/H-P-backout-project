#import libraries
from time import localtime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import mplcursors
from matplotlib.widgets import CheckButtons

#ask for file name
print("Enter CSV File Name: ") #filename should end in .csv or else file nopt found error will occur
inputFile = input() #gets input from user

#read the csv file
data = pd.read_csv(inputFile) 
print("Graphing " + inputFile + ".....") 

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

#multiple graphs (subplots)
fig, ax = plt.subplots()
ax2 = ax.twinx()

# LOAD DATA #
#time from the csv 
x = data.riglocaltime
x = np.asanyarray(x, dtype = 'datetime64[s]')

x1 = x[data.adpvdeltap >= 0]
y1 = data.adpvdeltap[data.adpvdeltap>= 0]

x2 = x[data.adpvtorque >= 0]
y2 = data.adpvtorque[data.adpvtorque >= 0]

x3 = x[data.adpvrop >= 0]
y3 = data.adpvrop[data.adpvrop >= 0]

x4 = x[data.adpvwob >= 0]
y4 = data.adpvwob[data.adpvwob >= 0]

y5 = data.bitdepth

y6 = data.bottomdepth

y7 = data.standpipepressure

# PLOT DATA #
l1, = ax.plot(x, data.hookload, 'deeppink', label='hookload')
l2, = ax.plot(x1, y1,'purple', label='adpvdeltap')
l3, = ax.plot(x2, y2, 'red', label='adpvtorque')
l4, = ax.plot(x3, y3, 'green', label='adpvrop')
l5, = ax.plot(x4, y4, 'blue', label='adpvwob')

l6, = ax2.plot(x, y5, 'navy', label='bitdepth')
l7, = ax2.plot(x, y6, 'gold', label='bottomdepth')
l8, = ax2.plot(x, y7, 'deepskyblue', label='standpipepressure')

#grab colors for check buttons
lines_by_label = {l.get_label(): l for l in [l1, l2, l3, l4, l5 ,l6, l7, l8]}
line_colors = [l.get_color() for l in lines_by_label.values()]

# Make checkbuttons with all plotted lines with correct visibility
rax = fig.add_axes([0.05, 0.4, 0.1, 0.15])
check = CheckButtons(
    ax=rax,
    labels=lines_by_label.keys(),
    actives=[l.get_visible() for l in lines_by_label.values()],
    label_props={'color': line_colors},
    frame_props={'edgecolor': 'black'},
    check_props={'facecolor': line_colors},
)

# callback for checkbuttons
def callback(label):
    ln = lines_by_label[label]
    ln.set_visible(not ln.get_visible())
    ln.figure.Canvas.draw_idle()
#check if clicked
check.on_clicked(callback)

#limits for y axis scale 2
#ax2.set_ylim(bottom=12000, top=36000)

#creates a grid behind lines
ax.grid()

#legend corresponding to each scale
ax.legend(loc='upper left')
ax2.legend(loc='upper right')

#title is name of the file
ax.set_title(inputFile, fontdict = font)

#annotated cursor - displays data at a single point when hovered over
cursor = mplcursors.cursor(hover=True)
#prompts matplotlib to open (displays your graph)
plt.show()

#ends the program when x button clicked in matplotlib graph
print("Graph closed. :)")
exit()