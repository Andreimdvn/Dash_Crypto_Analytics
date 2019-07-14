import os

import pandas as pd
import numpy as np


class CryptoRepo:
    def __init__(self, csv_file, model_folder='models', data_folder='data'):
        self.csv_file = csv_file
        self.__model_folder = model_folder
        self.__data_folder = data_folder
        self.__data = None
        self.__coins = None
        self.__load_data()
        print('CryptoRepo ready.')

    def __load_data(self):
        self.__data = pd.read_csv(self.csv_file)
        self.__coins = np.unique(self.__data['coin'])
        self.__data.set_index(['coin', 'type'], inplace=True)

    def get_coin_names(self):
        return self.__coins

    def get_data_file(self, coin):
        return os.path.join(self.__data_folder, self.__data.loc[coin, 1]['data_file'])

    def get_model_file_path(self, coin, type):
        file_name = self.__data.loc[coin, type]['model_file']
        for root, _, files in os.walk(self.__model_folder):
            for file in files:
                if file.startswith(file_name):
                    return os.path.join(root, file)

    def get_model_data(self, coin, type, data_column):
        return self.__data.loc[coin, type][data_column]
