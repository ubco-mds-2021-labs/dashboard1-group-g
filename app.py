#All import statements
import pandas as pd
import altair as alt
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from altair_data_server import data_server
import dash_bootstrap_components as dbc
from datetime import date
alt.data_transformers.disable_max_rows()


def top_n_by_popularity(data,ycol='Name'):
    """Makes a plot for the 10 most popular songs or artists. 
    Args:
        data (pandas.DataFrame): The filtered data frame you want the top songs/artists from. 
        ycol (str, optional): Can be either 'Artist' or 'Name', indicates which top 10 to plot. Defaults to 'Name'.
    Returns:
        html: An html page with the plot. 
    """    
    #data_filtered = data[["Name", "Artist","Popularity","Album Release Date"]]
    data_subset=data.groupby([ycol]).mean()
    data_subset = data_subset. reset_index()
    top10=data_subset.nlargest(10,'Popularity')
    chart = alt.Chart(top10).mark_bar().encode(
        alt.X('mean(Popularity)'),
        alt.Y(ycol,sort='-x')
        ).properties(
        width=400,
        height=200
    ).interactive()
    return chart.to_html()


def count_vs_year(data):
    """Plot the count of records released over time for each genre. 
    Args:
        data (pandas.DataFrame): The filtered data frame to plot information from. 
    Returns:
        html: An html page with the plot. 
    """    
    chart = alt.Chart(data).mark_line().encode(
        alt.X('Year'),
        alt.Y('sum(Number of Songs)', sort = '-x'),
        color=alt.Color('Playlist Genre')
    ).properties(
        width=400,
        height=200
    ).interactive()
    return chart.to_html()


def plot_subgenres(data):
    """Plot the count of records in subgenres for each genre. 
    Args:
        data (pandas.DataFrame): The filtered data frame to plot information from. 
    Returns:
        html: An html page with the plot. 
    """    
    chart = alt.Chart(data).mark_circle().encode(
        alt.X('Playlist Subgenre',title='Subgenre'),
        alt.Y('sum(Number of Songs)', sort = '-x'),
        color=alt.Color('Playlist Subgenre', legend = None),
        size=alt.Size('sum(Number of Songs)', legend = None),
        tooltip='sum(Number of Songs)'
    ).properties(
        width=500,
        height=100).interactive()
    return chart.to_html()

def pop_vs_year(data):
    """Plot the average popularity of records released over time for each genre. 
    Args:
        data (pandas.DataFrame): The filtered data frame to plot information from. 
    Returns:
        html: An html page with the plot. 
    """    
    chart = alt.Chart(data).mark_line().encode(
        alt.X('Year'),
        alt.Y('Mean Popularity'),
        color=alt.Color('Playlist Genre')
    ).properties(
        width=400,
        height=200
    ).interactive()
    return chart.to_html()

# Read in global data
topSongs = pd.read_csv('data/top_songs.csv', sep = '\t')
pd.to_datetime(topSongs["Year"], format='%Y')
topArtists = pd.read_csv('data/top_artists.csv', sep = '\t')
pd.to_datetime(topArtists["Year"], format='%Y')
topData = {"Name" : topSongs, "Artist": topArtists}
genreData =  pd.read_csv('data/genre_splits.csv', sep = '\t')
pd.to_datetime(genreData["Year"], format='%Y')

# Setup app and layout/frontend
app = Dash(__name__,  external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server 
header=html.Div([

        html.Div([], className = 'col-2'), #Same as img width, allowing to have the title centrally aligned

        html.Div([
            html.H1(children='Spotified',
                    style = {'textAlign' : 'center','color':'Green'}
            )],
            className='col-8',
            style = {'padding-top' : '2%'}
        ),

        html.Div([
            html.Img(
                    src = app.get_asset_url('logo1.png'),
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
                options=[{'label': i, 'value': i} for i in genreData['Playlist Genre'].unique()],
                value=[i for i in genreData['Playlist Genre'].unique()],
                multi=True,
                id = 'genre_widget') 
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

releasedate=html.Div([dbc.Row([html.Div([
                html.H3(children='Year of Album Release Date',
                    style = {'textAlign' : 'start','color':'black'}
            )],
            className='col-4',
            style = {'padding-top' : '1%'}
        ),
            dcc.RangeSlider(min=1957, max=2020,value = [1957, 2020], marks={i: str(i) for i in range(1957, 2021, 3)},id = 'release_year')
                    ])
   ]   ,className = 'row',
        style = {'height' : '2%',
                'background-color' : 'green'}
)

top10=html.Div([dbc.Row([html.Div([
                html.H3(children='Top 10 by',
                    style = {'textAlign' : 'start','color':'black'}
            )],
            className='col-4',
            style = {'padding-top' : '1%'}
        ),
            dcc.Dropdown(
            id='ycol', value='Name',
            options=[{'label': i, 'value': i} for i in ['Name','Artist']])
                    ])
   ]   ,className = 'row',
        style = {'height' : '2%',
                'background-color' : 'green'}
)

row1=html.Div([dbc.Row([
        dbc.Col(html.Iframe(
                id = 'top_n_plot', srcDoc= top_n_by_popularity(topData['Name'],ycol='Name'),
                style={'border-width': '0', 'width': '100%', 'height': '300px'}, 
        ), md = 6),
        dbc.Col(html.Iframe(
                id = 'timecountplot', srcDoc = count_vs_year(genreData),
                style={'border-width': '0', 'width': '100%', 'height': '300px'}
        ), md = 6)] 
        ), 
    ],
        className='row',
        style={'height':'2%','background-color' : 'gray'}                   
)

row2=html.Div([dbc.Row([
        dbc.Col(html.Iframe(
                id='subgenreplot',srcDoc=plot_subgenres(genreData),
                style={'border-width': '0', 'width': '100%', 'height': '300px','align-items' : 'end'} 
        ), md = 6),
        dbc.Col(html.Iframe(
                id='popvsyear',srcDoc=pop_vs_year(genreData),
                style={'border-width': '0', 'width': '100%', 'height': '300px','align-items' : 'end'}
        ), md = 6)] 
        ), 
    ],
        className='row',
        style={'height':'2%','background-color' : 'gray'}                   
)

app.layout = dbc.Container([header,genredrop,releasedate,top10,row1,row2])

#Set up callbacks/backend
@app.callback(
    Output('top_n_plot', 'srcDoc'),
    Output('timecountplot', 'srcDoc'),
    Output('subgenreplot','srcDoc'),
    Output('popvsyear','srcDoc'),
    Input('genre_widget', 'value'),
    Input('ycol', 'value'),
    Input('release_year', 'value'))

def plot_altair(genre_widget,ycol,release_year):
    """Update all four plots with the information from the widgets. 
    Args:
        genre_widget (list): List of genres to display from the genre dropdown. 
        ycol (string): Either 'Name' or 'Artist', indicates which top 10 to plot, from the top 10 by dropdown. 
        release_year (list)): List conatining start and end years, from the year slider. 
    Returns:
        list: A list with all four html plots. 
    """    
    newData = genreData.loc[genreData['Playlist Genre'].isin(genre_widget)]
    newData = newData.loc[(newData['Year'] >= release_year[0]) & (newData['Year'] <= release_year[1])]

    newTopData = topData[ycol]
    newTopData = newTopData.loc[newTopData['Playlist Genre'].isin(genre_widget)]
    newTopData = newTopData.loc[(newTopData['Year'] >= release_year[0]) & (newTopData['Year'] <= release_year[1])]

    return top_n_by_popularity(newTopData,ycol), count_vs_year(newData), plot_subgenres(newData), pop_vs_year(newData)


#Run in debug mode if it's running as the main program. 
if __name__ == '__main__':
    app.run_server(host='127.0.0.1',debug=True)