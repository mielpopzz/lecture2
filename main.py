import matplotlib.pyplot as plt
from math import sin, cos
import numpy as np
import csv
x1 = []
y1 = []
x2 = []
y2 = []
with open('bd-dec21-births-deaths-natural-increase.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['Births_Deaths_or_Natural_Increase'] == 'Births':
            y1.append(int(row['Count']))
            x1.append(int(row['Period']))
            print(int(row['Count']))
        elif row['Births_Deaths_or_Natural_Increase'] == 'Deaths':
            y2.append(int(row['Count']))
            x2.append(int(row['Period']))

x = np.linspace(2000,2023, 100)
y = (x-2010)**3+55*(x-2010)**2+45000
fig, ax = plt.subplots()
ax.plot(x, y, linewidth=2.0, label='(x-2010)**3+55*(x-2010)**2+45000')
ax.plot(x1, y1, label='Births')
ax.plot(x2, y2, label='Deaths')
ax.set_title('Births/Deaths')
ax.set_xlabel('Period')
ax.set_ylabel('Counts')
ax.legend()
plt.show()
