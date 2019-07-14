import os
import sys

sys.path.append(os.path.abspath('../repo_licenta'))

import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from Controller.CryptoController import CryptoController
from app import app
from dash.dependencies import Input, Output

controller = CryptoController('crypto_data.csv')

image_links = {
    "bat": 'https://s3-ap-southeast-1.amazonaws.com/cmf-image/Coin_inner/BAT.png',
    "xmr": 'https://assets.coingecko.com/coins/images/69/large/monero_logo.png?1547033729',
    "ltc": 'https://cdn.worldvectorlogo.com/logos/litecoin.svg',
    'eth': 'https://upload.wikimedia.org/wikipedia/commons/0/05/Ethereum_logo_2014.svg',
    "btc": 'http://pngimg.com/uploads/bitcoin/bitcoin_PNG38.png'
}

layout = html.Div(
    [html.Div([
        html.Span("CRYPTO - Trading Assistant", className='app-title'),
        html.Div(
            html.Img(src=image_links['bat'],
                     height="100%"),
            style={"float": "right", "height": "100%"}),
        html.Div(
            html.Img(src=image_links["xmr"],
                     height="100%"),
            style={"float": "right", "height": "100%"}),
        html.Div(
            html.Img(src=image_links['ltc'],
                     height="100%"),
            style={"float": "right", "height": "100%"}),
        html.Div(
            html.Img(src=image_links['eth'], height="100%"),
            style={"float": "right", "height": "100%"}),
        html.Div(
            html.Img(src=image_links["btc"], height="100%"),
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
        html.Link(
            href="https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css",
            rel="stylesheet")
        # html.Link(
        #     href="https://cdn.rawgit.com/amadoukane96/8a8cfdac5d2cecad866952c52a70a50e/raw/cd5a9bf0b30856f4fc7e3812162c74bfc0ebe011/dash_crm.css",
        #     rel="stylesheet")
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
                  colorway=["#5E0DAC", '#FF4F00', '#0af731', '#FF7400', '#FFF400', '#FF0056'],
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
    model1_data = controller.get_data_for_model(coin, 1)
    model2_data = controller.get_data_for_model(coin, 2)
    if model1_data["verdict"] != model2_data["verdict"]:
        overall_verdict = "NEUTRAL"
    else:
        overall_verdict = model1_data["verdict"]
    color_verdicts = {"SELL": "red", "BUY": "green", "NEUTRAL": "blue"}

    return html.Div(
        [
            html.Br(),
            html.H1("Overall"),
            html.Br(),
            html.H4("Current price: {:.2f}".format(model1_data["current_price"])),
            html.H4("Expecting price range: {:.2f}- {:.2f}".format(min(model1_data["tomorrow_price"], model2_data["tomorrow_price"]),
                                                                   max(model1_data["tomorrow_price"], model2_data["tomorrow_price"]))),
            html.H4("Prediction:"),
            html.H2(overall_verdict, style={"color": color_verdicts[overall_verdict]}),
            html.A('View on CoinMarketCap', href=controller.get_coin_link(coin), target="_blank", style={"font-size": "17px"}),
            html.Br(),
            html.Br(),
            html.Div(html.Img(src=image_links[coin], height="100%"), style={"height": "200px", "float": "down"}),
        ],
        className="four columns chart_div",
        style={"height": "700px", "text-align": "center"}
    )


def get_model_verdict(coin, type):
    model_data = controller.get_data_for_model(coin, type)
    verdict_color = "red" if model_data["verdict"] == "SELL" else "green"
    return html.Div(
        [
            html.H2(model_data["title"], style={"text-align": "center"}),
            html.P("Tomorrow prediction: {:.2f}".format(model_data["tomorrow_price"])),
            html.P("Current price: {:.2f}".format(model_data["current_price"])),
            html.P("Expected change: {0:.2f}".format(float(model_data["expected_change"]))),
            html.H3("Verdict: {}".format(model_data["verdict"]), style={"color": verdict_color, "text-align": "center"}),
            html.P("Predicting the next day closing price based on previous {} days".format(model_data["sequence_length"])),
            html.P("Testing accuracy: {}%".format(model_data["testing_accuracy"])),
            html.P("Used features: {}".format(model_data["features"]), className="model_text")
        ],
        className="six columns chart_div",
        style={"height": "370px"}
    )


def get_model_verdict_graph(coin, type):
    previous_prices, future_price = controller.get_model_future_prediction(coin, type)
    data = [go.Scatter(x=list(range(len(previous_prices))),
                       y=previous_prices,
                       mode='lines',
                       opacity=0.7,
                       name="{} Price".format(coin),
                       textposition='bottom center'),
            go.Scatter(x=[len(previous_prices)], y = [future_price], mode='markers', opacity=0.9, name="Tomorrow price")
            ]

    figure = {'data': data,
              'layout': go.Layout(
                  colorway=["#5E0DAC", '#FF4F00', '#0af731', '#FF7400', '#FFF400', '#FF0056'],
                  height=600,
                  title="Next day prediction of {}".format(coin),
                  xaxis={"title": "Days"},
                  yaxis={"title": "Price (USD)"}
              )
              }
    graph = dcc.Graph(id='{}-{}-graph'.format(coin, type), style={"height": "95%", "width": "98%",
                                                                  'margin-left': 'auto', 'margin-right': 'auto',
                                                                  'align': 'center'},
                      className='char_div', figure=figure)
    return html.Div(graph, className="six columns chart_div", style={"height": "700px"})


def get_model_history_points(coin, type):
    """
    Returns count DIVS with graphs with historical prices
    """
    historical_predictions = controller.get_model_historical_predictions(coin, type)
    return_divs = []
    for previous_prices, actual_price, predicted_price in historical_predictions:
        data = [go.Scatter(x=list(range(len(previous_prices))),
                           y=previous_prices,
                           mode='lines',
                           opacity=0.7,
                           name="{} Price".format(coin),
                           textposition='bottom center'),
                go.Scatter(x=[len(previous_prices)], y=[actual_price], mode='markers', opacity=0.9,
                           name="Actual price"),
                go.Scatter(x=[len(previous_prices)], y=[predicted_price], mode='markers', opacity=0.9,
                           name="Predicted price")
                ]

        figure = {'data': data,
                  'layout': go.Layout(
                      colorway=["#5E0DAC", '#FF4F00', '#0af731', '#FF7400', '#FFF400', '#FF0056'],
                      height=600,
                      title="Historic model prediction for {}".format(coin),
                      xaxis={"title": "Days"},
                      yaxis={"title": "Price (USD)"}
                  )
                  }
        graph = dcc.Graph(id='{}-{}-{}-graph'.format(coin, type, len(return_divs)), style={"height": "95%", "width": "98%",
                                                                      'margin-left': 'auto', 'margin-right': 'auto',
                                                                      'align': 'center'},
                          className='char_div', figure=figure)
        return_divs.append(html.Div(graph, className="six columns chart_div", style={"height": "700px"}))

    return return_divs


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
            get_model_verdict(coin, 1),
            get_model_verdict(coin, 2)
        ],
        className="row",
        style={"marginTop": "5px"}
    )


def get_next_history_rows(coin):
    model1_h = get_model_history_points(coin, 1)
    model2_h = get_model_history_points(coin, 2)
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
            get_model_verdict_graph(coin, 1),
            get_model_verdict_graph(coin, 2)
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
    print("Updating page with new coin: {}".format(selected_dropdown_value))
    return html.Div(id='main_div', children=[get_first_row(coin), get_second_row(coin), get_third_row(coin),
                                             get_history_title_row()] + get_next_history_rows(coin))
