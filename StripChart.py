import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
#import pyodbc

fig = plt.figure(figsize=(10, 3))
gs = fig.add_gridspec(11, hspace=0)
axs = gs.subplots(sharex=True, sharey=False)

font = {'family': 'serif',
        'color':  'black',
        'weight': 'normal',
        'size': 16,
        }

#ask for file name
print("Enter CSV File Name: ")
inputFile = input()

#read the csv file
data = pd.read_csv(inputFile)

print("Graphing " + inputFile + ".....") 

x = data.riglocaltime
x = np.asanyarray(x, dtype = 'datetime64[s]')


axs[0].set_title(inputFile, fontdict = font)

axs[0].plot(x, data.hookload, 'red', label='hookload')

axs[1].plot(x, data.Wraps, 'darkorange', label='Wraps')

axs[2].plot(x, data.tdoscltoffset, 'gold', label='tdoscltoffset')
axs[2].plot(x, data.tdoscltfwdpossp, 'forestgreen', label='tdoscltfwdpossp')
axs[2].plot(x, data.tdoscltrevrossp, 'lightseagreen', label='tdoscltrevrossp')

axs[3].plot(x, data.topdrivespeed,'dodgerblue', label='topdrivespeed')
axs[3].plot(x, data.elevatorposition, 'blue', label='elevatorposition')

axs[4].plot(x, data.topdrivetorque, 'blueviolet', label='topdrivetorque')

axs[5].plot(x, data.bitdepth, 'mediumorchid', label='bitdepth')
axs[5].plot(x, data.bottomdepth, 'deeppink', label='bottomdepth')

axs[6].plot(x, data.adpvrop, 'greenyellow', label='adpvrop')
axs[6].plot(x, data.adsprop, 'royalblue', label='adsprop')

axs[7].plot(x, data.adpvwob, 'coral', label='adpvwob')
axs[7].plot(x, data.adspwob, 'mediumvioletred', label='adspwob')

axs[8].plot(x, data.adpvdeltap, 'darkturquoise', label='adpvdeltap')
axs[8].plot(x, data.adspdeltap, 'springgreen', label='adspdeltap')

axs[9].plot(x, data.standpipepressure, 'purple', label='standpipepressure')

axs[10].step(x, data.tdmodestate, 'navy', label='tdmodestate')


axs[0].set_ylabel('hookload', rotation='horizontal')
axs[1].set_ylabel('Avg Wraps', rotation='horizontal')
axs[2].set_ylabel('Wraps & Offset', rotation='horizontal')
axs[3].set_ylabel('RPM & Elevator Position', rotation='horizontal')
axs[4].set_ylabel('Torque', rotation='horizontal')
axs[5].set_ylabel('Depth', rotation='horizontal')
axs[6].set_ylabel('ROP', rotation='horizontal')
axs[7].set_ylabel('WOB', rotation='horizontal')
axs[8].set_ylabel('Delta P', rotation='horizontal')
axs[9].set_ylabel('SPP', rotation='horizontal')
axs[10].set_ylabel('TD Mode State', rotation='horizontal')

axs[10].set_xlabel('time')



for i in range(11):
  axs[i].legend(bbox_to_anchor=(1.005, 1), loc='upper left', borderaxespad=0)
  axs[i].yaxis.set_label_coords(-.1, .1)
  axs[i].grid()


plt.show()
