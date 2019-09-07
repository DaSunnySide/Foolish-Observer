import pandas as pd
import plotly.graph_objects as go
import plotly.offline as pyo
from pandas.io.json import json_normalize
import plotly.tools as tools

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

#Get user input for stock choice and function information
symbol = input('Stock Symbol: \n')
datatype = 'datatype=csv'

function = input("Function: \n")
if function== 'TIME_SERIES_INTRADAY' :
    interval = input('Time interval in minutes: \n')
    symbol = symbol + '&interval=' + interval + 'min'

#Define Api call
API_KEY = 'VW506K51LFXGUT1C'
API_QUERY = 'https://www.alphavantage.co/query?function=' + function + '&symbol=' + symbol + '&' + 'apikey=' + API_KEY+'&' +datatype

#Define Dataframe and resolve issues with Intraday graph range
if function == 'TIME_SERIES_INTRADAY' :
    df = pd.read_csv(API_QUERY)

else:
    df = pd.read_csv(API_QUERY)

graph_options=[
            {'label': 'Time Series Intraday', 'value' : 'TIME_SERIES_INTRADAY'},
            {'label': 'Time Series Daily', 'value' : 'TIME_SERIES_DAILY'},
            {'label': 'Time Series Daily Adjusted', 'value' : 'TIME_SERIES_DAILY_ADJUSTED'},
            {'label': 'Time Series Weekly', 'value' : 'TIME_SERIES_WEEKLY'},
            {'label': 'Time Series Weekly Adjusted', 'value' : 'TIME_SERIES_WEEKLY_ADJUSTED'},
            {'label': 'Time Series Monthly', 'value' : 'TIME_SERIES_MONTHLY'},
            {'label': 'Time Series Monthly Adjusted', 'value' : 'TIME_SERIES_MONTHLY_ADJUSTED'}
        ]
fig = go.Figure(data=[go.Candlestick(x=df['timestamp'],
                                     open=df['open'],
                                     high=df['high'],
                                     low=df['low'],
                                     close=df['close'],
                                     increasing_line_color='#4DFF4D',
                                     decreasing_line_color='#193EFD'
                                     )
              ])



if __name__ == '__main__':
    fig.show()
