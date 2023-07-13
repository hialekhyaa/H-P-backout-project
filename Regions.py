import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
 
inputFile = "regions.csv" 
data = pd.read_csv(inputFile) 

x = ['NORTH', 'SOUTH', 'EAST', 'WEST']
y = []

count = 0
index = 0
for j in x :
    for i in data.Region :
        if (i == j) :
            count = count + 1
    y.insert(index, count)
    count = 0
    index = index + 1
print(y)
  
fig, ax = plt.subplots()
ax.pie(y, labels=x, autopct='%1.1f%%', colors=['palegreen', 'cornflowerblue', 'plum', 'pink'])

plt.show()

