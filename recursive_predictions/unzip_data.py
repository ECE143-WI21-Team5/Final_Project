import zipfile
import urllib.request
import os

year = 2010
data_path = '\\Users\\jesus\\OneDrive\\Desktop\\ECE_143\\ozone_data\\'
for i in range(10):
    pass
    url = 'https://aqs.epa.gov/aqsweb/airdata/daily_44201_'+str(year)+'.zip'
    print(url)
    urllib.request.urlretrieve(url, data_path+'ozone_data'+str(year)+'.zip')
    with zipfile.ZipFile(data_path+'ozone_data'+str(year)+'.zip', 'r') as zip_ref:
        zip_ref.extractall(data_path+str(year)+'_data')
    
    os.remove(data_path+'ozone_data'+str(year)+'.zip') 

    year +=1
