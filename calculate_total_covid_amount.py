import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

def total_covid_cases(route):

    f =open(route)


    q = f.readlines()
    q1 = []
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

    plt.title('CA new covid cases VS date')
    plt.xlabel('Date')
    plt.ylabel('New Cases')
    plt.yticks(np.arange(0,60000,10000))
    plt.xticks(np.arange(0,1000,90))
    plt.plot(date, amount)

    pop = 39984261
    x = 0
    for a in amount:
        if date[x] == date[-1]:
            break
        if a/pop < 1/100000:
            plt.axvspan(date[x],date[x+1], facecolor='#ecec09', alpha=0.5)
        if 1/100000 <= a/pop < 4/100000:
            plt.axvspan(date[x],date[x+1], facecolor='#e34100', alpha=0.5)
        if 4/100000 <= a/pop <= 7/100000:
            plt.axvspan(date[x],date[x+1], facecolor='#fe0000', alpha=0.5)
        if a/pop > 7/100000:
            plt.axvspan(date[x],date[x+1], facecolor='#a00039', alpha=0.5)
        x += 1
    # print(pop/100000*1)

    plt.show()



