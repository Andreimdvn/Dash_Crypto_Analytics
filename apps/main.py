import os
import sys

import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from Controller.CryptoController import CryptoController
from app import app
from dash.dependencies import Input, Output

sys.path.append(os.path.abspath('../repo_licenta'))

controller = CryptoController('crypto_data.csv')

layout = html.Div(
    [html.Div([
        html.Span("CRYPTO - Trading Assistant", className='app-title'),
        html.Div(
            html.Img(src='https://s3-ap-southeast-1.amazonaws.com/cmf-image/Coin_inner/BAT.png',
                     height="100%"),
            style={"float": "right", "height": "100%"}),
        html.Div(
            html.Img(src='https://assets.coingecko.com/coins/images/69/large/monero_logo.png?1547033729',
                     height="100%"),
            style={"float": "right", "height": "100%"}),
        html.Div(
            html.Img(src='https://cdn.worldvectorlogo.com/logos/litecoin.svg',
                     height="100%"),
            style={"float": "right", "height": "100%"}),
        html.Div(
            html.Img(src='https://upload.wikimedia.org/wikipedia/commons/0/05/Ethereum_logo_2014.svg', height="100%"),
            style={"float": "right", "height": "100%"}),
        html.Div(
            html.Img(src='http://pngimg.com/uploads/bitcoin/bitcoin_PNG38.png', height="100%"),
            style={"float": "right", "height": "100%"})
    ],
        className="row header"
    ),
        html.Div([
            dcc.Tabs(
                id="tabs",
                style={"height": "20", "verticalAlign": "middle"},
                children=[
                    dcc.Tab(label="Bitcoin", value="btc"),
                    dcc.Tab(label="Ethereum", value="eth"),
                    dcc.Tab(label="Litecoin", value="ltc"),
                    dcc.Tab(label="Monero", value="xmr"),
                    dcc.Tab(label="Basic Attention Token", value="bat")
                ],
                value="btc",
            )
        ],
            className="row tabs_div"
        ),
        html.Div(id="current_prediction", style={"margin": "2% 3%"}, className="row")
     ], className="body")


def get_price_graph(coin):
    price_data = controller.get_coin_data(coin)
    data = [go.Scatter(x=price_data["Date"],
                       y=price_data["price(USD)"],
                       mode='lines',
                       opacity=0.7,
                       name="{} Price".format(coin),
                       textposition='bottom center')
            ]

    figure = {'data': data,
              'layout': go.Layout(
                  colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
                  height=600,
                  title="Price of {}".format(coin),
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
    return dcc.Graph(id='my-graph', style={'width': '50%', 'height': '50%', 'margin-left': 'auto', 'margin-right': 'auto', 'align': 'center'}, className='char_div', figure=figure)


@app.callback(Output('current_prediction', 'children'),
              [Input('tabs', 'value')])
def update_graph(selected_dropdown_value):
    coin = selected_dropdown_value
    print('wtf')
    return html.Div(id='main_div', children=[get_price_graph(coin)])
