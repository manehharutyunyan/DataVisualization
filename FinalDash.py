import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# file paths
ru_videos_filepath = "C:/Users/maneh_onrsjft/Downloads/DataVizualization/HomeworkProject/archive/RUvideos.csv"
ca_videos_filepath = "C:/Users/maneh_onrsjft/Downloads/DataVizualization/HomeworkProject/archive/CAvideos.csv"
de_videos_filepath = "C:/Users/maneh_onrsjft/Downloads/DataVizualization/HomeworkProject/archive/DEvideos.csv"
fr_videos_filepath = "C:/Users/maneh_onrsjft/Downloads/DataVizualization/HomeworkProject/archive/FRvideos.csv"
gb_videos_filepath = "C:/Users/maneh_onrsjft/Downloads/DataVizualization/HomeworkProject/archive/GBvideos.csv"
in_videos_filepath = "C:/Users/maneh_onrsjft/Downloads/DataVizualization/HomeworkProject/archive/INvideos.csv"
jp_videos_filepath = "C:/Users/maneh_onrsjft/Downloads/DataVizualization/HomeworkProject/archive/JPvideos.csv"
kr_videos_filepath = "C:/Users/maneh_onrsjft/Downloads/DataVizualization/HomeworkProject/archive/KRvideos.csv"
mx_videos_filepath = "C:/Users/maneh_onrsjft/Downloads/DataVizualization/HomeworkProject/archive/MXvideos.csv"
us_videos_filepath = "C:/Users/maneh_onrsjft/Downloads/DataVizualization/HomeworkProject/archive/USvideos.csv"

# Read the file into a variable 
v_ru = pd.read_csv(ru_videos_filepath, parse_dates=True, encoding='latin1')
v_ca = pd.read_csv(ca_videos_filepath, parse_dates=True, encoding='latin1') 
v_de = pd.read_csv(de_videos_filepath, parse_dates=True, encoding='latin1') 
v_fr = pd.read_csv(fr_videos_filepath, parse_dates=True, encoding='latin1')
v_gb = pd.read_csv(gb_videos_filepath, parse_dates=True, encoding='latin1')
v_in = pd.read_csv(in_videos_filepath, parse_dates=True, encoding='latin1')
v_jp = pd.read_csv(jp_videos_filepath, parse_dates=True, encoding='latin1')
v_kr = pd.read_csv(kr_videos_filepath, parse_dates=True, encoding='latin1')
v_mx = pd.read_csv(mx_videos_filepath, parse_dates=True, encoding='latin1')
v_us = pd.read_csv(us_videos_filepath, parse_dates=True, encoding='latin1')

#Add column with name of country in all datasets
v_ru['Country'] = 'Russia'
v_ca['Country'] = 'Canada'
v_de['Country'] = 'Germany'
v_fr['Country'] = 'France'
v_gb['Country'] = 'Great Britain'
v_in['Country'] = 'India'
v_jp['Country'] = 'Japan'
v_kr['Country'] = 'Italy'
v_mx['Country'] = 'Mexico'
v_us['Country'] = 'United States'

# concatenate all videos  in a one table
#all_video = pd.concat([v_ru, v_ca, v_de, v_fr, v_gb, v_gb, v_in, v_jp, v_kr, v_mx, v_us])
all_video = pd.concat([v_ru, v_ca, v_us])
all_video[pd.isnull(all_video.views)]
all_video['Title Length'] = all_video.title.apply(lambda p:len(p))

# clean data
all_video = all_video.drop(['video_id', 'trending_date','tags','title', 'channel_title', 'category_id', 'thumbnail_link', 'ratings_disabled', 'video_error_or_removed', 'description', 'comments_disabled'],axis=1)

all_video = all_video['views'] = all_video[ all_video['views'] < 4000000 ]
all_video = all_video['likes'] = all_video[ all_video['likes'] < 100000 ]
all_video = all_video['dislikes'] = all_video[ all_video['dislikes'] < 7000 ]
all_video = all_video['comment_count'] = all_video[ all_video['comment_count'] < 15000 ]

all_video = all_video.rename(columns={'publish_time': 'Publish Time',
                                      'views' : 'Views',
                                      'likes':'Likes',
                                      'dislikes':'Dislikes',
                                      'comment_count':'Comments Count'})


# take year from 'Publish time'
all_video['Publish Time'] = all_video['Publish Time'].str.slice(start=0, stop=4)

# createing options list
num_cols = ['Views','Likes', 'Dislikes', 'Comments Count', 'Title Length']
year_cols = ['2017', '2018', 'All']
year_cols_2 = ['2017', '2018']


# columns for correlation heatmap
corrCol=['Views','Likes','Dislikes','Comments Count', 'Title Length']
corrData = all_video[corrCol].corr()

features = [{'label': i, 'value': i} for i in all_video.columns]
years = [{'label': i, 'value': i} for i in year_cols]
num_options = [{'label': i, 'value': i} for i in num_cols]

features = [{'label': i, 'value': i} for i in all_video.columns]
years = [{'label': i, 'value': i} for i in year_cols]
num_options = [{'label': i, 'value': i} for i in num_cols]
years_2 = [{'label': i, 'value': i} for i in year_cols_2]

# dash processing
app = dash.Dash(__name__)

app.layout = html.Div([
            html.Div([html.H1('Correlation Heatmap')], className = 'row'),
            html.Div([
                   html.Div(
                            dcc.Checklist(
                                            id='correnation',
                                            options=[{'label': x, 'value': x} for x in corrData.columns],
                                            value=corrData.columns.tolist(),
                                        ),
                           className = 'twelve columns'),
                ], className = 'row'),
            html.Div([
                   html.Div([dcc.Graph(id="graph")], className = 'twelve columns'),
            ], className = 'row'),


            html.Div([dcc.Dropdown(
                                id = 'features_input',
                                options = features, value = features[2]['value'], className='six columns'),
                     dcc.Dropdown(
                                id = 'years_input',
                                options = years, value = years[0]['value'], className='six columns')],
                 
                 className = 'twelve columns'),
            html.Div([
                   html.Div([dcc.Graph(id='Fig1')], className = 'twelve columns'),
            ], className = 'row'),

            html.Div([dcc.Dropdown(
                                id = 'var1',
                                options = num_options, value = num_options[0]['value'], className='six columns'),
                     dcc.Dropdown(
                                id = 'var2',
                                options = num_options, value = num_options[1]['value'], className='six columns')],
                 className = 'twelve columns'),
            html.Div([
                   html.Div([dcc.Graph(id='Fig3')], className = 'twelve columns'),
            ], className = 'row'),
            

            html.Div([dcc.Dropdown(
                                id = 'var6',
                                options = num_options, value = num_options[0]['value'], className='six columns')],
                 
                 className = 'twelve columns'),
            html.Div([
                   html.Div([dcc.Graph(id='Fig5')], className = 'twelve columns'),
            ], className = 'row')
                  
         ], className = 'container')


# heatmap
@app.callback(
    Output("graph", "figure"), 
    [Input("correnation", "value")])
def filter_heatmap(cols):
    fig = px.imshow(corrData.loc[cols, cols])
    return fig


# hist
@app.callback(
       Output(component_id = 'Fig1', component_property = 'figure'),
        [Input(component_id = 'features_input', component_property = 'value'),
         Input(component_id = 'years_input', component_property = 'value')]         
)
def update_hist(input_1, input_2):
    # if(input_2 != 'All'):
    #     data = all_video[all_video['Publish Time'] == int(input_2)]
    # else:
    data = all_video
        
    figure_1 = px.histogram(data, x=input_1, title='Distribution of {}'.format(input_1), nbins=50)
    return figure_1


# scatter
@app.callback(
       Output(component_id = 'Fig3', component_property = 'figure'),
         [Input(component_id = 'var1', component_property = 'value'),
          Input(component_id = 'var2', component_property = 'value')]
)
def update_scatter(input_3, input_4):
    figure_2 = px.scatter(all_video, x=input_3, y=input_4, title='Scatter plot of {} and {} variables'.format(input_3, input_4))
    return figure_2

# map
@app.callback(
    Output(component_id = 'Fig5', component_property = 'figure'),
       [Input(component_id = 'var6', component_property = 'value')] 
)
def update_map(input_2):
    groups = all_video.groupby('Country')
    grouppedData = groups.first()

    data = go.Choropleth(
    locations =  grouppedData.index,
    locationmode = 'country names',
    z = grouppedData[input_2],
    marker = go.choropleth.Marker(
        line = go.choropleth.marker.Line(
            color = 'rgb(255, 255, 255)',
            width = 1.5,
        )
    ),
    colorbar = go.choropleth.ColorBar(
        title = input_2
        )
    )

    layout = go.Layout(
        geo = go.layout.Geo(
            showlakes = True,
            lakecolor = 'rgb(255, 255, 255)'
        )
    )

    fig = go.Figure(data = data, layout = layout)
    return fig

if __name__ == '__main__':
    app.run_server(debug = True)