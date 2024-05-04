import os
import requests
import pandas as pd


class Stock:
    """Get stock data"""

    API_KEY = os.getenv("POLYGON_API_KEY")

    def __init__(self, ticker):
        self.ticker = ticker
        self.df = self.make_stock_df()

    def get_daily_stock_prices(self, ticker):
        if not isinstance(ticker, str):
            raise TypeError("Ticker must be a string.")
        try:
            url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/2021-05-01/2024-01-01?sort=asc&apiKey={Stock.API_KEY}"
            r = requests.get(url)
            data = r.json()
            return data
        except:
            raise ValueError

    def make_stock_df(self):
        data = self.get_daily_stock_prices(self.ticker)
        ticker = data["ticker"]
        df = pd.DataFrame(data["results"])
        df["ticker"] = ticker
        df["date"] = pd.to_datetime(df["t"], unit="ms")
        df.set_index("date", inplace=True)
        df.index = pd.to_datetime(df.index.date)
        return df


# class Index:
#     """Get index data"""

#     API_KEY = os.getenv("FRED_API_KEY")

#     def __init__(self, ticker):
#         self.ticker = ticker
#         self.df = self.make_stock_df()
