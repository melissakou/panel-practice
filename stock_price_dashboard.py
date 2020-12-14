import os
import datetime
import panel as pn
import pandas as pd
import panel.widgets as pnw
import plotly.graph_objects as go

pn.extension("plotly")

files = os.listdir('data')
AAFMG = []
for f in files:
    data = pd.read_csv('data/' + f)
    data['Symbol'] = f.replace('.csv', '')
    AAFMG.append(data)
AAFMG = pd.concat(AAFMG)
AAFMG['Date'] = pd.to_datetime(AAFMG['Date'])

# Create Widget Components
symbol = pnw.Select(name = 'symbol', options = ['AAPL', 'AMZN', 'FB', 'GOOGL', 'MSFT'])
value = pnw.RadioButtonGroup(name = 'value', options = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
window = pnw.IntSlider(name = 'window', start = 7, end = 365, value = 30)
date_range = pnw.DateRangeSlider(name = 'date range',
                                 start = datetime.datetime(1980, 12, 12), end = datetime.datetime(2020, 4, 1),
                                 value = (datetime.datetime(2017, 4, 1), datetime.datetime(2020, 4, 1)))

# Define Reactive Plot Function
@pn.depends(symbol, value, window, date_range)
def reactive_plot(symbol, value, window, date_range):
    df = AAFMG.loc[AAFMG['Symbol'] == symbol]
    df = df.sort_values('Date')
    df['MA'] = df[value].rolling(window = window).mean()
    df = df.loc[(df['Date'] >= date_range[0]) & (df['Date'] <= date_range[1])]
    
    fig = go.Figure(layout = go.Layout(plot_bgcolor = '#EEEEEE'))
    fig.add_trace(go.Scatter(
        x = df["Date"], y = df[value],
        name = '%s/%s' %(symbol, value),
        fill = 'tozeroy',
        line_width = 0,
        line_color = 'rgba(72,89,110,1)',
        fillcolor = 'rgba(72,89,110,0.8)',
    ))
    fig.add_trace(go.Scatter(
        x = df["Date"], y = df["MA"],
        name = '%s/%s/MA%d' %(symbol, value, window),
        mode = "lines",
        line_color = '#a57571',
        line_width = 2.5
    ))
    fig.update_layout(
        width = 600, height = 400,
        margin=dict(l = 20, r = 20, t = 20, b = 20),
        legend = dict(
            orientation = "h",
            yanchor = "bottom",
            y = 1.02,
            xanchor = "right",
            x = 1
        )
    )
    
    return fig

text = "# Stock Market Data\nSelect a symbol, value, and the time window for moving average"
widgets = pn.Column(text, symbol, value, window, date_range)
dashboard = pn.Row(reactive_plot, widgets)

dashboard.servable();