import zipfile
import urllib.request
import os
import matplotlib.pyplot as plt
from datetime import timezone
from datetime import datetime
from pandas.plotting import register_matplotlib_converters
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.tsa.statespace.sarimax import SARIMAX
register_matplotlib_converters()
from time import time
import numpy as np
import itertools
import csv

def download_data(year, data_path, dataType):
    """
    This functions downloads the data from the EPA website in a starting year and 
    puts it into a folder.
    input: int, str, str
    output: None
    """
    assert(isinstance(year, int)), "not a year number"
    assert(isinstance(data_path, str)), "not a folderLocation"
    assert(isinstance(dataType, str)), "the data type is not a string"
    if(dataType == "ozone"):
        website_sub_place = "44201"
    elif(dataType == "SO2"):
        website_sub_place = "42401"
    elif(dataType == "CO"):
        website_sub_place = "42101"

    for i in range(2021-year):
        pass
        url = 'https://aqs.epa.gov/aqsweb/airdata/daily_'+website_sub_place+'_'+str(year)+'.zip'
        print(url)
        urllib.request.urlretrieve(url, data_path+ dataType +'_data'+str(year)+'.zip')
        with zipfile.ZipFile(data_path+dataType +'_data'+str(year)+'.zip', 'r') as zip_ref:
            zip_ref.extractall(data_path+str(year)+'_data')
        
        os.remove(data_path+dataType +'_data'+str(year)+'.zip') 

        year +=1

def convine_data_files(start_year, data_path, dataType):
    """
    This functions convines the data of the years of a specific data type
    input: year, data_path, data_type
    output: list
    """
    assert(isinstance(start_year, int)), "not a year number"
    assert(isinstance(data_path, str)), "not a folderLocation"
    assert(isinstance(dataType, str)), "the data type is not a string"

    if(dataType == "ozone"):
        website_sub_place = "44201"
    elif(dataType == "SO2"):
        website_sub_place = "42401"
    elif(dataType == "CO"):
        website_sub_place = "42101"

    year = start_year
    lines = []
    for i in range(2021-start_year):
        with open(data_path+str(year)+'_data'+'\\daily_'+website_sub_place+'_'+str(year)+'.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for line in list(reader):
                lines.append(line)
        year += 1
    return lines

def filter_counties(environmental_dataset, county_sample):
    county_data = []
    for i in county_sample:
        county_data.append(city_regression(environmental_dataset,i))
    print(len(county_data))
    return county_data

class city_regression:
    """
    Contains the data for specific cities
    """
    def __init__(self, data, city_name):
        self.city_name = city_name
        self.data = []
        self.data_float = []
        added_dates = []
        for ind_measurment in data:
            if(city_name in ind_measurment):
                temp = [datetime.strptime(ind_measurment[11],"%Y-%m-%d"),float(ind_measurment[16])]
                if(str(datetime.strptime(ind_measurment[11],"%Y-%m-%d")) not in added_dates):
                    added_dates.append(str(datetime.strptime(ind_measurment[11],"%Y-%m-%d")))
                    self.data.append(temp)
                    self.data_float.append([datetime.strptime(ind_measurment[11],"%Y-%m-%d").timestamp(),float(ind_measurment[16])])
              
    def __str__(self):
        return str(self.city_name)
    def print_graph(self):
        a = np.asarray(self.data)

        x, y = a.T
        y = np.convolve(y, np.ones(30), 'valid') / 7
        y = list(itertools.islice(y,0,len(y)-1,7))
        x = list(itertools.islice(x,0,len(x)-1,7))
        print(len(x[0:-4]), len(y))
        plt.plot(x[0:-4],y)
        plt.show()
        
def choose_dataset(dataType):
    """
    returns the counties of california that actually have the data
    input: str
    output: list
    """
    assert(isinstance(dataType,str)), "the datatype must be a string"
    if(dataType == "CO"):
        county_sample =['Alameda','Butte','Contra Costa', 'Fresno','Humboldt', 'Kern', 'Los Angeles', 'Marin', 'Monterey', 'Napa','Orange','Riverside', 'Sacramento', 'San Bernardino', 'San Diego', 'San Francisco', 'San Mateo', 'Santa Barbara', 'Sonoma', 'Stanislaus']
    elif(dataType == "SO2"):
        county_sample = ["San Diego"]
    elif(dataType == "ozone"):
        county_sample  =['Alameda','Amador','Butte', 'Calaveras','Colusa', 'Contra Costa', 'El Dorado', 'Glenn', 'Humboldt', 'Imperial', 'Inyo','Kern', 'Kings', 'Lake', 'Los Angeles', 'Madera', 'Marin', 'Mariposa', 'Mendocino', 'Merced', 'Monterey', 'Napa','Nevada', 'Orange', 'Placer','Riverside', 'Sacramento', 'San Benito', 'San Bernardino']
    
    return county_sample

def print_raw_county_data(county_data):
    """
    prints out a graph of the raw county data
    input: list
    output: none   
    """
    for i in county_data:
        a = np.asarray(i.data)

        x, y = a.T  
        print(i)
        plt.plot(x,y)
        plt.show()

def prepare_county_data(county_data, county_sample, start_year, end_year):
    """
    Prepares the data for the predictions
    input: list(data)
    output: list(test dates), list(total train data), list(test data)   
    """
    train_data_convined = []
    test_data = []
    test_dates = []
    k = 0
    for i in county_data:
        a = np.asarray(i.data)
        x, y = a.T
        y = np.convolve(y, np.ones(30), 'valid') / 7
        y = list(itertools.islice(y,0,len(y)-1,7))
        x = list(itertools.islice(x,0,len(x)-1,7))

        minDate = 1
        maxDate = 1

        while True:
            try:
                print(x.index(datetime(end_year,1,minDate)))
                break
            except:
                minDate = minDate +1
        while True:
            try:
                print(x.index(datetime(start_year,1,maxDate)))
                break
            except:
                maxDate = maxDate +1

        trainData = (x[x.index(datetime(start_year,1,maxDate)):x.index(datetime(end_year,1,minDate))],y[x.index(datetime(start_year,1,maxDate)):x.index(datetime(end_year,1,minDate))])

        plt.figure(figsize=(15,7))
        plt.plot(trainData[0],trainData[1])
        plt.xlabel('Date')
        plt.ylabel('Parts Per Million')
        plt.title('Pollution per date '+county_sample[k])

        plt.show()
        train_data_convined.append(trainData)
        test_data.append(y[x.index(datetime(end_year,1,minDate))+1:])
        test_dates.append(x[-len(test_data[-1]):])
        print(len(test_data[-1]), len(test_dates[-1]))
        k = k + 1
    return test_dates, train_data_convined, test_data

def make_predictions(train_data_convined,test_dates):
    predictions = []
    print("predictions to be made ",len(train_data_convined))
    k = 0
    for i in train_data_convined:
        my_order = (0,1,0)
        my_seasonal_order = (1, 0, 1, 52.143)
        # define model
        model = SARIMAX(i[1], order=my_order, seasonal_order=my_seasonal_order)
        model_fit = model.fit()
        predictions.append(model_fit.forecast(len(test_dates[k])))
        print(k, " counties predicted")
        k = k +1
    return predictions

def print_predictions(data_name, predictions,test_dates, county_sample):
    k = 0
    for i in predictions:
        plt.plot(test_dates[k],i)
        plt.xlabel('Date')
        plt.ylabel('Parts Per Million')
        plt.title(data_name + ' pollution prediction ' + county_sample[k])
        plt.show()
        k = k + 1

def print_test_data(data_name, test_data,test_dates, county_sample):
    k = 0
    for i in test_data:
        plt.plot(test_dates[k],i)
        plt.xlabel('Date')
        plt.ylabel('Parts Per Million')
        plt.title(data_name + ' pollution date ' + county_sample[k])
        plt.show()
        k = k + 1

def print_residuals(test_data, predictions, county_sample,test_dates):
    residuals = []
    for i in range(len(test_data)):
        residuals.append(test_data[i] - predictions[i])
        plt.figure(figsize=(10,4))
        plt.plot(test_dates[i],residuals[i])
        plt.axhline(0, linestyle='--', color='k')
        plt.title('Residuals from SARIMA Model ' + county_sample[i], fontsize=20)
        plt.ylabel('Difference vs Expected', fontsize=16)

def print_difference(data_name,test_data,predictions,test_dates,county_sample):
    print(len(test_data), len(predictions))
    k = 0
    for i in range(len(test_data)):

        plt.figure(figsize=(15,7))
        plt.plot(test_dates[i],predictions[i], label = "Predicted PPM") 
        plt.plot(test_dates[i],test_data[i], label = "Actual PPM") 
        plt.legend()
        plt.title(data_name + ' pollution to Date ' + county_sample[i])
        plt.xlabel('Date')
        plt.ylabel('Parts Per Million')
        plt.show()
        k = k + 1