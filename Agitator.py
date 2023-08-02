import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
 
inputFile = "agit.csv" 
data = pd.read_csv(inputFile) 

x = ['Y', 'N']
y = []

count = 0
index = 0
for j in x :
    for i in data.Agitator :
        if (i == j) :
            count = count + 1
    y.insert(index, count)
    count = 0
    index = index + 1
print(y)
  
fig, ax = plt.subplots()
ax.pie(y, labels=['Used Agitator', 'Agitator Not Used'], autopct='%1.1f%%', colors=['lightgreen', 'lightskyblue'])

plt.show()

