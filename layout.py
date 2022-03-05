#All import statements
from ctypes import alignment
from tkinter import N
import pandas as pd
import altair as alt
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from datetime import date
from xml.dom.minidom import CharacterData
alt.data_transformers.enable('data_server')
alt.data_transformers.disable_max_rows()


#fetching data and wrangling data for visualization
def getSpotifyData():
    data = pd.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-01-21/spotify_songs.csv')
    data = data.dropna()
    data = data.drop(['track_id', 'track_album_id', 'playlist_id'], axis=1)
    data.columns = ["Name", "Artist", "Popularity", "Album Name", "Album Release Date", "Playlist Name", 
                "Playlist Genre", "Playlist Subgenre", "Danceability", 
               "Energy", "Key", "Loudness", "Mode", "Speechiness", 
               "Acousticness", "Instrumentalness", "Liveness", "Valence", 
              "Tempo", "Duration"]
    data['Playlist Genre'] = data['Playlist Genre'].str.title()
    data['Playlist Subgenre'] = data['Playlist Subgenre'].str.title()
    mode = {1 : 'Major', 0:'Minor'}
    key = {0 : 'C', 1:'C#', 2: 'D', 3:'D#', 4: 'E', 5:'F', 6: 'F#', 7:'G', 
           8: 'G#', 9:'A', 10: 'Bb', 11:'B'}
    data.replace({"Mode":mode}, inplace = True)
    data.replace({"Key":key}, inplace = True)
    return data

#Placeholder until actual plots are ready. 
def plot(data):
    chart = alt.Chart(data).mark_line().encode(
        alt.X('year(Album Release Date)'),
        alt.Y('count(Name)',sort='-x'),
        color=alt.Color('Playlist Genre')
    ).properties(
        width=800,
        height=450
    ).interactive()
    return chart.to_html()

##plot of subgenres for the genre selected.
def subplot(data):
    chart = alt.Chart(data).mark_circle().encode(
        alt.X('Playlist Subgenre',title='Subgenre'),
        alt.Y('count(Name)',sort='-x',title='Number of Records'),
        color=alt.Color('Playlist Subgenre'),
        size=alt.Size('count(Name)'),
        tooltip='count(Playlist Subgenre)'
    ).properties(
        width=500,
        height=400).interactive()
    return chart.to_html()




# Read in global data
data = getSpotifyData()

# Setup app and layout/frontend
app = Dash(__name__,  external_stylesheets=[dbc.themes.BOOTSTRAP])
header=html.Div([

        html.Div([], className = 'col-2'), #Same as img width, allowing to have the title centrally aligned

        html.Div([
            html.H1(children='Spotify',
                    style = {'textAlign' : 'center','color':'Green'}
            )],
            className='col-8',
            style = {'padding-top' : '2%'}
        ),

        html.Div([
            html.Img(
                    src = app.get_asset_url('logo.png'),
                    height = '50 px',
                    width = 'auto')
            ],
            className = 'col-2',
            style = {
                    'align-items': 'center',
                    'padding-top' : '2%',
                    'height' : 'auto'})

        ],
        className = 'row',
        style = {'height' : '4%',
                'background-color' : 'Black'}
        )
#creating one more dropdown


genredrop= html.Div([dbc.Row([html.Div([
            html.H3(children='Genre',
                    style = {'textAlign' : 'start','color':'black'}
            )],
            className='col-2',
            style = {'padding-top' : '1%'}
        ),
            html.Div([dcc.Dropdown(
                options=[{'label': i, 'value': i} for i in data['Playlist Genre'].unique()],
                value=[i for i in data['Playlist Genre'].unique()],
                multi=True,
                id = 'genre-widget') 
            ], className='col-5',
                     style={'height' : '2%',
                'background-color' : 'black','align-items' : 'end'}
            )       
        ])
],
        className = 'row',
        style = {'height' : '2%',
                'background-color' : 'green'}
)

popularitybar=html.Div([dbc.Row([html.Div([
                html.H3(children='Popularity Rating',
                    style = {'textAlign' : 'start','color':'black'}
            )],
            className='col-4',
            style = {'padding-top' : '1%'}
        ),
            dcc.RangeSlider(min=0, max=100, marks={0: '0', 50: '50', 100:'100'}, value = [0, 100], id = 'popularity-widget')
        ])
   ]   ,className = 'row',
        style = {'height' : '2%',
                'background-color' : 'green'}
)
plot2=html.Div([dbc.Row(html.Iframe(
                id = 'timecountplot', srcDoc = plot(data),
                style={'border-width': '0', 'width': '100%', 'height': '600px'}
        ),
                 className='col-10',
              style = {'padding-top' : '1%'}       
              
        )
    ],
        className='row',
               style={'height':'2%','background-color' : 'gray'}       
               
)

plot3=html.Div([dbc.Row(html.Iframe(id='subgenreplot',srcDoc=subplot(data),
                  style={'border-width': '0', 'width': '100%', 'height': '600px','align-items' : 'end'}
        ),
                        className='col-7',
              style = {'padding-top' : '1%'}
)
],
               className='row',
               style={'height':'2%','background-color' : 'gray'}
)

app.layout = dbc.Container([header,genredrop,popularitybar,plot2,plot3])

#Set up callbacks/backend
@app.callback(
    Output('timecountplot', 'srcDoc'),
    Output('subgenreplot','srcDoc'),
    Input('genre-widget', 'value'),
    Input('popularity-widget', 'value'))
def plot_altair(genres, popularity):
    newData = data.loc[data['Playlist Genre'].isin(genres)]
    newData = data.loc[(data['Popularity'] >= popularity[0]) & (data['Popularity'] <= popularity[1])]
    newData1 = data.loc[data['Playlist Genre'].isin(genres)]
    return plot(newData), subplot(newData1)



if __name__ == '__main__':
    app.run_server(debug=True)