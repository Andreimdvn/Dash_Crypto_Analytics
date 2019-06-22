import os

import pandas as pd
import numpy as np


class CryptoRepo:
    def __init__(self, csv_file, model_folder='models', data_folder='data'):
        self.csv_file = csv_file
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
