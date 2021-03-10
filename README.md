# Final_Project

### Presentation pdf file

- ECE 143 Group 5 Project.pdf

### Jupyter notebook file

- final_submission.ipynb

### Third-party modules used

- pandas
- numpy
- matplotlib
- seaborn
- folium
- statsmodels

### File structure

- datasets
  - o3.csv
  - co.csv
  - pm25.csv
  - statewide_cases.csv
  
- calculate_total_covid_amount.py
  - combines all the increase covid-19 cases data of each countries in California  
- air_quality_trend.py
  - run plot_aqi_trend(air quality DataFrame, covid DataFrame, AQI column name) to see plot
- quick_COVID_lockdown_timeline.py
  - creates a timeline of COVID lockdown events in California
- final_regression.py
  - filters out for data in california
  - runs filters on that that
  - runs SARIMAX models
  - plots the prediction vs actual
- draw_choropleth.py
  - draws choropleth map from the results of SARIMAX models 
  - demo in draw_choropleth_map.ipynb
- counties.json
  - geometric information of California counties for choropleth maps
### How to run code
-SARIMAX Predictive model
  - Should be able to run it straight. Do make sure that the folder where the data is to be stored exists
  - eg. in the current code. the folder '/air_quality/CO' folder should exist
