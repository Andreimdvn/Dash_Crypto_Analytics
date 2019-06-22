import pandas as pd

from Repository.CryptoRepo import CryptoRepo


class CryptoController:

    def __init__(self, csv_path: str):
        self.repo = CryptoRepo(csv_path)
        self.__price_data = self.load_price_data()  # dict of df
        print("CryptoController ready.")

    def get_coin_data(self, coin):
        return self.__price_data[coin]

    def load_price_data(self):
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
