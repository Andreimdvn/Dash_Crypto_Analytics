import random

import pandas as pd
import numpy as np

from data_loading import data_loader_factory
from model.LSTM_model import LstmModel
from Repository.CryptoRepo import CryptoRepo


class CryptoController:
    MODEL_TYPES = [1, 2]
    HISTORY_POINTS = 5

    def __init__(self, csv_path: str):
        self.repo = CryptoRepo(csv_path)
        self.__price_data = self.__load_price_data()  # dict of df
        self.__models_history_predictions = {}
        self.__models_future_prediction = {}
        self.__load_models_prediction()
        print("CryptoController ready.")

    def get_coin_data(self, coin):
        return self.__price_data[coin]

    def get_overall_verdict(self, coin):
        return "wtf"

    def get_model_future_prediction(self, coin, type):
        return self.__models_future_prediction[(coin, type)]

    def get_model_historical_predictions(self, coin, type):
        return self.__models_history_predictions[(coin, type)]

    def __load_price_data(self):
        price_data = {}
        all_coins = self.repo.get_coin_names()

        for coin in all_coins:
            price_file = self.repo.get_data_file(coin)
            raw_data = pd.read_csv(price_file)
            raw_data = raw_data.dropna()
            raw_data['Date'] = pd.to_datetime(raw_data.date, infer_datetime_format=True)
            price_data[coin] = raw_data
            print("{} data loaded.".format(coin))

        return price_data

    def __load_models_prediction(self):
        for coin in self.repo.get_coin_names():
            for type in self.MODEL_TYPES:
                model_file = self.repo.get_model_file_path(coin, type)
                data_file = self.repo.get_data_file(coin)
                days_to_predict = 100
                sequence_length = self.repo.get_model_data(coin, type, "sequence_length")
                multiple_features = True if type is 2 else False
                self.__models_history_predictions[(coin, type)], self.__models_future_prediction[(coin, type)] = \
                    self.__get_model_history_predictions_and_future_prediction(model_file, data_file, days_to_predict,
                                                                               sequence_length, multiple_features)
                print("History for {} {} loaded".format(coin, type))

    def __get_model_history_predictions_and_future_prediction(self, model_file, data_file, days_to_predict,
                                                              sequence_length, multiple_features):
        data_loader = data_loader_factory.get_data_loader(data_file, days_to_predict, False,
                                                          sequence_length, False,
                                                          multiple_features=multiple_features)
        lstm_model = LstmModel()
        lstm_model.load_from_file(model_file)

        y_predicted = lstm_model.test_model(data_loader.x_test)
        actual = data_loader.reverse_min_max_y(np.reshape(data_loader.y_test, (len(data_loader.y_test), 1)))
        predicted = data_loader.reverse_min_max_y(y_predicted)

        reshaped_x_test = np.reshape(data_loader.x_test, (
            data_loader.x_test.shape[0] * data_loader.x_test.shape[1], data_loader.x_test.shape[2]))
        actual_price_input = data_loader.reverse_min_max(reshaped_x_test)
        actual_price_input = np.reshape(actual_price_input, data_loader.x_test.shape)[:, :, 0]

        future_prediction = (actual_price_input[-1], predicted[-1])
        historical_predictions = self.__get_history_predictions(actual_price_input[:-1], actual[:-1], predicted[:-1])
        lstm_model.delete()

        return historical_predictions, future_prediction

    def __get_history_predictions(self, input_prices, actual_price, predicted_price):
        indexes = list(range(len(input_prices)))
        random.shuffle(indexes)

        historical_predicitions = []
        rand_idx = 0
        for current in range(self.HISTORY_POINTS):
            idx = indexes[rand_idx]
            historical_predicitions.append((input_prices[idx], actual_price[idx], predicted_price[idx]))
            rand_idx += 1

        return historical_predicitions

    def get_data_for_model(self, coin, type):
        p0 = self.__models_future_prediction[(coin, type)][0][-1]
        p1 = self.__models_future_prediction[(coin, type)][1]
        d = {
             "title": "Model {} - {}".format(type, "based on price" if type == 1 else "based on price and other features"),
             "current_price": p0,
             "tomorrow_price": p1,
             "expected_change": p1 / p0 - 1,
             "verdict": "BUY" if p1 > p0 else "SELL",
             "sequence_length": self.repo.get_model_data(coin, type, "sequence_length"),
             "testing_accuracy": self.repo.get_model_data(coin, type, "acc"),
             "features": self.repo.get_model_data(coin, type, "columns")}
        return d

    def get_coin_link(self, coin):
        return self.repo.get_model_data(coin, 1, "link")
