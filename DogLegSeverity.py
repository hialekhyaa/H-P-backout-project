from time import localtime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import mplcursors
from matplotlib.widgets import CheckButtons

inputFile = "DLS.csv" 

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

# PLOT DATA #
l1, = ax.plot(data.depthR390, data.dlsR390, '-o', color='deepskyblue', label='R390')
l2, = ax.plot(data.depthR261, data.dlsR261, '-o', color='mediumvioletred', label='R261')
l3, = ax.plot(data.depthR535, data.dlsR535, '-o', color='gold', label='R535')
l4, = ax.plot(data.depthR641, data.dlsR641, '-o', color='deeppink', label='R641')
l5, = ax.plot(data.depthR384b1, data.dlsR384b1, '-o', color='orangered', label='R384b1')
l6, = ax.plot(data.depthR384b2, data.dlsR384b2, '-o', color='forestgreen', label='R384b2')
l7, = ax.plot(data.depthR503, data.dlsR503, '-o', color='purple', label='R503')
l8, = ax.plot(data.depthR607, data.dlsR607, '-o', color='blue', label='R607')

#grab colors for check buttons
lines_by_label = {l.get_label(): l for l in [l1, l2, l3, l4, l5, l6, l7, l8]}
line_colors = [l.get_color() for l in lines_by_label.values()]

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


#title is name of the file
ax.set_title("Depth vs DLS", fontdict = font)

#annotated cursor - displays data at a single point when hovered over
cursor = mplcursors.cursor(hover=True)
#prompts matplotlib to open (displays your graph)
plt.show()

#ends the program when x button clicked in matplotlib graph
print("Graph closed. :)")
exit()