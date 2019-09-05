import plotly.graph_objs as go
import pandas as pd
import plotly.graph_objs as go
import plotly.offline as pyo
from pandas.io.json import json_normalize
import plotly.tools as tools
import dash
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

#Initialize App
app = dash.Dash()

#Define Colors for the UI
colors = {
    'dashbg' : '#2F3036',
    'graphbg' : '#151515',
    'increasingline' : '#4dff4d',
    'decreasingline' : '#193EFD',
    'lowcontrasttext' : '#585A65',
    'highcontrasttext' : '#FAFAFF'
}

#Define Alpha Vantage Function Calls
TIME_SERIES_INTRADAY = 'TIME_SERIES_INTRADAY'
TIME_SERIES_DAILY = 'TIME_SERIES_DAILY'
TIME_SERIES_DAILY_ADJUSTED = 'TIME_SERIES_DAILY_ADJUSTED'
TIME_SERIES_WEEKLY = 'TIME_SERIES_WEEKLY'
TIME_SERIES_WEEKLY_ADJUSTED = 'TIME_SERIES_WEEKLY_ADJUSTED'
TIME_SERIES_MONTHLY = 'TIME_SERIES_MONTHLY'
TIME_SERIES_MONTHLY_ADJUSTED = 'TIME_SERIES_MONTHLY_ADJUSTED'

#Read in stock symbols...
nsdq = pd.read_csv('nsdq.csv')
nyse = pd.read_csv('nyse.csv')

nsdq.set_index('Symbol', inplace=True)
nyse.set_index('Symbol', inplace=True)
options = []

for tic in nsdq.index:
    options.append({'label':'{} {}'.format(tic, nsdq.loc[tic]['Name']), 'value':tic})

for tic in nyse.index:
    options.append({'label': '{} {}'.format(tic, nyse.loc[tic]['Name']), 'value':tic})


#Array with options to alter graph type within plotly
graph_options=[
            {'label': 'Time Series Intraday', 'value' : 'TIME_SERIES_INTRADAY'},
            {'label': 'Time Series Daily', 'value' : 'TIME_SERIES_DAILY'},
            {'label': 'Time Series Daily Adjusted', 'value' : 'TIME_SERIES_DAILY_ADJUSTED'},
            {'label': 'Time Series Weekly', 'value' : 'TIME_SERIES_WEEKLY'},
            {'label': 'Time Series Weekly Adjusted', 'value' : 'TIME_SERIES_WEEKLY_ADJUSTED'},
            {'label': 'Time Series Monthly', 'value' : 'TIME_SERIES_MONTHLY'},
            {'label': 'Time Series Monthly Adjusted', 'value' : 'TIME_SERIES_MONTHLY_ADJUSTED'}
        ]

#Set the application layout
app.layout = html.Div(([

    #Dropdown menu for stock selection
    html.Div([
        dcc.Dropdown(
        id='stock-symbol',
        options=options,
        value='MSFT',
        multi=True)
        ], style={'display': 'flex', 'verticalAlign':'top', 'width':'30%'}),

    #Dropdown menu for graph type
    html.Div([
        dcc.Dropdown(
            id='graph-type',
            options=graph_options,
            value='TIME_SERIES_DAILY'
    )
    ], style={'display': 'flex', 'verticalAlign':'top', 'width':'30%'}),

    #Submit button to render the graphs again
    html.Div([
        html.Button(
            id='submit-button',
            children='Submit',
            n_clicks=0,
            style={'fontSize':24, 'marginLeft':'30px'}
        )
    ], style={'display': 'flex', 'verticalAlign': 'top', 'width': '30%'}),
    #Display candlestick graph
    html.Div([
        dcc.Graph(id='candlestick',
                      figure={

                      })

    ])

]))

#Update graphs based on new graph and stock selection
def generateCandleStick(symbol, function):
    #Run the API_QUERY Every time the graph must be updated, then generate the graph with the information returned. Use pandas to generate a new dataframe that the graph will display.

    #Get all variables for the query from the user inputs on the page.
    stock = symbol
    graph = function
    datatype = 'datatype=csv'
    API_KEY = 'VW506K51LFXGUT1C'
    API_QUERY = 'https://www.alphavantage.co/query?function=' + graph + '&symbol=' + stock + '&' + 'apikey=' + API_KEY+'&' +datatype

    #Generate dataframe
    df = pd.read_csv(API_QUERY)
    print(df)
    print('test')

    #Use dataframe to generate graph
    return {
    'data': [
        go.Candlestick(x=df['timestamp'],
                       open=df['open'],
                       high=df['high'],
                       low=df['low'],
                       close=df['close'],
                       increasing_line_color='#4DFF4D',
                       decreasing_line_color='#193EFD'
                       )
    ],
      'layout': go.Layout(title='Candlestick Graph of prices of ${stock} over time')
}
@app.callback([Output('candlestick', 'figure')],
              [Input('stock-symbol', 'value'),
              Input('graph-type', 'value')])

if __name__ == '__main__':
    app.run_server()
