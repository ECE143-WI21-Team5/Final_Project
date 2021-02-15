import datetime
import csv
class city_regression:
    def __init__(self, data, city_name):
        self.data = []
        for ind_measurment in data:
            if(city_name in ind_measurment):
                self.data.append(ind_measurment)
    def __str__(self):
        return str(self.data[1])


def convine_data_files():
    data_path = '\\Users\\jesus\\OneDrive\\Desktop\\ECE_143\\ozone_data\\'
    year = 2010
    lines = []
    for i in range(10):
        with open(data_path+str(year)+'_data'+'\\daily_44201_'+str(year)+'.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for line in list(reader):
                lines.append(line)
        year += 1
    return lines

lines = convine_data_files()
aCity = city_regression(lines,"Baldwin")
print(aCity)