import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from app import app
from dash.dependencies import Input, Output

btc_df = pd.read_csv('datasets/bitcoin_datahub.csv')
btc_df = btc_df.dropna()
btc_df['Date'] = pd.to_datetime(btc_df.date, infer_datetime_format=True)


layout = html.Div(
    [html.H1("Cryptocurrencies Prices", style={'textAlign': 'center'}),
     dcc.Dropdown(id='my-dropdown',
                  options=[{'label': 'Bitcoin', 'value': 'BTC'},
                           {'label': 'Ripple', 'value': 'XRP'},
                           {'label': 'Ethereum', 'value': 'ETH'}],
                  multi=False,
                  value=['BTC'],
                  style={"display": "block",
                         "margin-left": "auto",
                         "margin-right": "auto",
                         "width": "60%"}),
     dcc.Graph(id='my-graph')
     ], className="container")


@app.callback(Output('my-graph', 'figure'),
              [Input('my-dropdown', 'value')])
def update_graph(selected_dropdown_value):
    # make data list?
    data = [go.Scatter(x=btc_df["Date"],
                      y=btc_df["price(USD)"],
                      mode='lines',
                      opacity=0.7,
                      name="{} Price".format(selected_dropdown_value),
                      textposition='bottom center')]

    figure = {'data': data,
              'layout': go.Layout(
                  colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
                  height=600,
                  title="Price of {}".format(selected_dropdown_value),
                  xaxis={"title": "Date",
                         'rangeselector':
                             {'buttons': list([{'count': 1, 'label': '1M', 'step': 'month', 'stepmode': 'backward'},
                                               {'count': 6, 'label': '6M', 'step': 'month', 'stepmode': 'backward'},
                                               {'step': 'all'}])},
                         'rangeslider': {'visible': True},
                         'type': 'date'},
                  yaxis={"title": "Price (USD)"}
              )
              }
    return figure
