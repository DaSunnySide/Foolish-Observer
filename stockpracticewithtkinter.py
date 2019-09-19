import pandas as pd
from pandas.io.json import json_normalize
import tkinter as tk
from tkinter import Menu
from tkinter import ttk
import matplotlib as plt
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from mpl_finance import candlestick_ohlc

#Define API Query
API_KEY = 'VW506K51LFXGUT1C'
function = 'TIME_SERIES_DAILY'
symbol = 'MSFT'
API_QUERY = 'https://www.alphavantage.co/query?function={}&symbol={}&apikey=' + API_KEY+'&csv'.format(function, symbol)

df = pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&apikey=VW506K51LFXGUT1C&datatype=csv')
print(df)

#Display Linegraph
linegraph = plt.plot(df['timestamp'], df['close'])

plt.xlabel('Date')
plt.ylabel('Close Price')
plt.title("Time series of {}".format(symbol))
plt.savefig('Simple Graph for AAPL.png')
#graph.grid(column=0, row=3, sticky="W")

#Display Candlestick Graph
#ohlc = df[['timestamp', 'open', 'high', 'low', 'close']].copy()

#f1, ax = plt.subplots(figsize=(10,5))

#candlestick_ohlc(ax, oh1c.values, width=.6, colorup='green', colordown='red')
#ax.axis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

#Window Design
def _quit():
    win.quit()
    win.destroy()
    exit()

win = tk.Tk()

#Define button input update
def updateInput():
    symbol = stockInput.get("1.0", END)
    function = functionInput.get("1.0", END)
    print(symbol, function)

menuBar = Menu()
win.config(menu=menuBar)
win.geometry("500x500")

fileMenu = Menu(menuBar, tearoff=0)
fileMenu.add_command(label="New")
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=_quit)
menuBar.add_cascade(label="File", menu=fileMenu)

tabControl = ttk.Notebook(win)

tab1 = ttk.Frame(tabControl)
tabControl.add(tab1, text="Chart of {}".format(symbol))

tabControl.pack(expand=1, fill="both")
graph_frame = ttk.LabelFrame(tab1, text="Graph of {}".format(symbol))
graph_frame.grid(column=0, row=1, padx=8, pady=4)

#Get user Input for stock symbol
ttk.Label(graph_frame, text="Stock symbol:").grid(column=0, row=0, sticky="W")
stockInput = ttk.Entry(graph_frame, width=30).grid(column=1, row=0, sticky="W")
ttk.Button(graph_frame, text="Submit", command=updateInput).grid(column=2, row=0, sticky="W")

#Get user input for function type
functiontype = tk.StringVar()
ttk.Label(graph_frame, text = "Function Type:").grid(column=0, row=1, sticky="W")
functionInput = ttk.Combobox(graph_frame, width=30, textvariable='functiontype')
functionInput['values'] = ('TIME_SERIES_INTRADAY', 'TIME_SERIES_DAILY', 'TIME_SERIES_DAILY_ADJUSTED',
                           'TIME_SERIES_WEEKLY', 'TIME_SERIES_WEEKLY_ADJUSTED', 'TIME_SERIES_MONTHLY',
                           'TIME_SERIES_MONTHLY_ADJUSTED')
functionInput.grid(column=1, row=1)
functionInput.current(0)

graphDisplay = plt.show()
graphDisplay.grid(column=2, row = 0)

win.mainloop()
