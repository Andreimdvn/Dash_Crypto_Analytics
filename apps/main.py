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
HISTORY_POINTS = 5

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
        html.Div(id="current_prediction", style={"margin": "2% 3%"}, className="row"),
        html.Link(href="https://use.fontawesome.com/releases/v5.2.0/css/all.css", rel="stylesheet"),
        html.Link(
            href="https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css",
            rel="stylesheet"),
        html.Link(href="https://fonts.googleapis.com/css?family=Dosis", rel="stylesheet"),
        html.Link(href="https://fonts.googleapis.com/css?family=Open+Sans", rel="stylesheet"),
        html.Link(href="https://fonts.googleapis.com/css?family=Ubuntu", rel="stylesheet"),
        html.Link(
            href="https://cdn.rawgit.com/amadoukane96/8a8cfdac5d2cecad866952c52a70a50e/raw/cd5a9bf0b30856f4fc7e3812162c74bfc0ebe011/dash_crm.css",
            rel="stylesheet")
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
    graph = dcc.Graph(id='my-graph', style={"height": "95%", "width": "98%", 'margin-left': 'auto',
                                            'margin-right': 'auto', 'align': 'center'},
                      className='char_div', figure=figure)
    return html.Div(graph, className="eight columns chart_div", style={"height": "700px"})


def get_overall_verdict(coin):
    return html.Div(
        [
            html.P(
                "Overall verdict",
            ),
            html.P(
                controller.get_overall_verdict(coin),
            ),
        ],
        className="four columns chart_div",
        style={"height": "700px"}
    )


# TO DO
def get_trash(coin):
    return html.Div(
        [
            html.P(
                "Overall verdict",
            ),
            html.P(
                controller.get_overall_verdict(coin),
            ),
        ],
        className="six columns chart_div",
        style={"height": "700px"}
    )


# TO DO
def get_model_verdict(coin, type):
    return get_trash(coin)


# TO DO
def get_model_verdict_graph(coin, type):
    return get_trash(coin)


# TO DO
def get_model_history_points(coin, type, count):
    return [get_trash(coin)] * count


def get_first_row(coin):
    return html.Div(
        [
            get_overall_verdict(coin),
            get_price_graph(coin)
        ],
        className="row",
        style={"marginTop": "5px"}
    )


def get_second_row(coin):
    return html.Div(
        [
            get_model_verdict(coin, 0),
            get_model_verdict(coin, 1)
        ],
        className="row",
        style={"marginTop": "5px"}
    )


def get_next_history_rows(coin, history_count):
    model1_h = get_model_history_points(coin, 0, history_count)
    model2_h = get_model_history_points(coin, 1, history_count)
    divs = []
    for h1, h2 in zip(model1_h, model2_h):
        divs.append(
            html.Div(
                [
                    h1, h2
                ],
                className="row",
                style={"marginTop": "5px"}
            )
        )
    return divs


def get_third_row(coin):
    return html.Div(
        [
            get_model_verdict_graph(coin, 0),
            get_model_verdict_graph(coin, 1)
        ],
        className="row",
        style={"marginTop": "5px"}
    )


def get_history_title_row():
    return html.Div(
        [html.H2("HISTORICAL PREDICTIONS", style={"text-align": "center"})],
        style={"marginTop": "5px"},
        className = "twelve columns header",
    )


@app.callback(Output('current_prediction', 'children'),
              [Input('tabs', 'value')])
def update_page(selected_dropdown_value):
    coin = selected_dropdown_value
    print('wtf')
    return html.Div(id='main_div', children=[get_first_row(coin), get_second_row(coin), get_third_row(coin),
                                             get_history_title_row()] +
                                            get_next_history_rows(coin, HISTORY_POINTS))
