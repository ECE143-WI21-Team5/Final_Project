import folium

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