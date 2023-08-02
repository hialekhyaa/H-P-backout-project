#import libraries
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import mplcursors
from matplotlib.widgets import CheckButtons

#file name
inputFile = "setpoints.csv"

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
plt.rc('xtick', labelsize=15)    
plt.rc('ytick', labelsize=18)    
plt.rc('legend', fontsize=12) 

#multiple graphs (subplots)
fig, ax = plt.subplots()
ax2 = ax.twinx()

# LOAD DATA #

#x axis is Rig number
x = data.rig

# PLOT DATA #
l1, = ax.plot(x, data.torque, 'o-', color='blue', label='torque')
l2, = ax.plot(x, data.speed, 'o-', color='violet', label='topdrivespeed')
l3, = ax2.plot(x, data.depth, 'o-', color='forestgreen', label='Depth')
l4, = ax.plot(x, data.fwdwraps, 'o-', color='deeppink', label='Forward Wraps')
l5, = ax.plot(x, data.revwraps, 'o-', color='darkorange', label='Reverse Wraps')
l6, = ax.plot(x, data.offset, 'o-', color='maroon', label='Offset')
l7, = ax.plot(x, data.bitsize, 'o-', color='deepskyblue', label='Bit Size')
l8, = ax.plot(x, data.pipesize, 'o-', color='purple', label='Pipe Size')

#grab colors for check buttons
lines_by_label = {l.get_label(): l for l in [l1, l2, l3, l4, l5, l6, l7, l8]}
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

#annotations for each point - adding or subtracting from v specifies the location of the displayed number
#for i, v in enumerate(data.torque):
    #ax.text(i, v+2, "%d" %v, ha="center", color='blue')
#for i, v in enumerate(data.speed):
    #ax.text(i, v+2, "%d" %v, ha="center", color='violet')
#for i, v in enumerate(data.depth):
    #ax2.text(i, v+4, "%d" %v, ha="center", color='forestgreen')
#for i, v in enumerate(data.revwraps):
    #ax.text(i, v+2, "%d" %v, ha="center", color='darkorange')
#for i, v in enumerate(data.fwdwraps):
    #ax.text(i, v-2, "%d" %v, ha="center", color='deeppink')
#for i, v in enumerate(data.offset):
    #ax.text(i, v-2, "%d" %v, ha="center", color='maroon')
#for i, v in enumerate(data.bitsize):
    #ax.text(i, v+1, "%d" %v, ha="center", color='deepskyblue')
#for i, v in enumerate(data.pipesize):
    #ax.text(i, v+1, "%d" %v, ha="center", color='purple')

#creates a grid behind lines
ax.grid()

#legend corresponding to each scale
ax.legend(bbox_to_anchor=(-0.05, 1), loc='upper right', borderaxespad=0)
ax2.legend(bbox_to_anchor=(1.005, 1), loc='upper left', borderaxespad=0)

#title is name of the file
ax.set_title(inputFile, fontdict = font)

#annotated cursor - displays data at a single point when hovered over
cursor = mplcursors.cursor(hover=True)
#prompts matplotlib to open (displays your graph)
plt.show()

#ends the program when x button clicked in matplotlib graph
print("Graph closed. :)")
exit()