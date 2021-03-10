import folium
import pandas as pd
from datetime import datetime

def draw_choropleth(data, col, legend):
    '''
    This function draws a choropleth map of California
    Parameters
    ----------
    data : pandas.DataFrame
        The pandas Dataframe, first column should be county names
    col : list
        names to two columns, one is county name, the other is the data to plot.
    legend : str
        legend of the data.

    Returns
    -------
    None.

    '''
    m = folium.Map(location=(37, -120), zoom_start=6)
    geo = 'counties.json'

    folium.Choropleth(geo_data=geo,
        data=data,
        columns=col,
        key_on='feature.properties.NAME',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        highlight=True,
        legend_name=legend
    ).add_to(m)
    folium.TileLayer('stamentoner').add_to(m)
    display(m)
    
def plot_map(test_data, predictions, county_sample,test_dates):
    residuals = []
    data_for_plot = {'county':[], 'date':[], 'residual':[]}
    for i in range(len(test_data)):
        residual = test_data[i] - predictions[i]
        residuals.append(residual)
        for j in range(len(residual)):
            data_for_plot['county'].append(county_sample[i])
            data_for_plot['date'].append(test_dates[i][j])
            data_for_plot['residual'].append(residual[j])
    df=pd.DataFrame(data_for_plot)
    for m in [2,3,4,5,6]:
        data_plt = df[df['date'] < datetime(2020,m,21,0,0)]
        data_plt = data_plt[data_plt['date'] > datetime(2020,m,15,0,0)]
        data_plt = data_plt.append(pd.DataFrame([['Alpine', datetime(2020,m,14,0,0), -0.06]], columns=['county', 'date', 'residual']), ignore_index=True)
        data_plt = data_plt.append(pd.DataFrame([['Del Norte', datetime(2020,m,14,0,0), 0.07]], columns=['county', 'date', 'residual']), ignore_index=True)
        col = ['county', 'residual']
        legend = 'Residual for '+ datetime(2020, m, 1).strftime("%B") +', 2020'
        draw_choropleth(data_plt, col, legend)