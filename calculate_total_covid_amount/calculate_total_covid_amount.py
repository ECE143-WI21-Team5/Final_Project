import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime


####

f =open(r"C:\Users\Administrator\Desktop\workspace\143 data\000/statewide_cases.csv")

####

q = f.readlines()
q1 = []
print(q[0])
for lines in q:
    line = lines.split(',')
    q1.append(line) 
q1 = q1[1:]

q2 = []
for lines in q1:
    lines[-1] = lines[-1][0:len(lines[-1]) - 1]
c0 = {}

# when select = 1 total confirmed
# when select = 2 total death
# when select = 3 new confirmed
# when select = 4 new death

select = 3
for lines in q1:
    if lines[-1] not in c0.keys():
        c0[lines[-1]] = int(lines[select])
    else:
        c0[lines[-1]] += int(lines[select])

date = list(c0.keys())
amount = list(c0.values())


# c0 format  key: '2020-05-21' value: XXXX 



i = 0
for dates in date:
    if dates == '2020-12-24' :
        print(i)
        break
    i += 1

# '2020-08-28'   -- 163 
# '2020-12-24'   -- 281



ax = plt.subplot(111) 
plt.plot(date, amount)

ymajorLocator = MultipleLocator(10000) # Y ticks
ax.yaxis.set_major_locator(ymajorLocator)

xmajorLocator = MultipleLocator(108) # X ticks
ax.xaxis.set_major_locator(xmajorLocator)

#plt.axvspan(date[163],date[281], facecolor='#2ca02c', alpha=0.5)
#plt.axvspan(date[620],date[705], facecolor='#ff0000', alpha=0.5)

plt.show()




