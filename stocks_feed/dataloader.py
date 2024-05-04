import os
import requests
import pandas as pd


class Stock:
    """Get stock data"""

    API_KEY = os.getenv("POLYGON_API_KEY")

    def __init__(self, ticker, start_date, end_date):
        if not isinstance(ticker, str):
            raise TypeError("Ticker must be a string.")
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.df = self.make_stock_df()

    def get_daily_stock_prices(self):
        try:
            url = f"https://api.polygon.io/v2/aggs/ticker/{self.ticker}/range/1/day/{self.start_date}/{self.end_date}?sort=asc&apiKey={Stock.API_KEY}"
            r = requests.get(url)
            data = r.json()
            return data
        except:
            raise ValueError

    def make_stock_df(self):
        data = self.get_daily_stock_prices()
        ticker = data["ticker"]
        df = pd.DataFrame(data["results"])
        df["ticker"] = ticker
        df["date"] = pd.to_datetime(df["t"], unit="ms")
        df.set_index("date", inplace=True)
        df.index = pd.to_datetime(df.index.date)
        df = self.get_daily_return(df)
        return df

    def get_daily_return(self, df):
        df["close_lag_1"] = df["c"].shift(periods=1)
        df["daily_return"] = (df["c"] / df["close_lag_1"]) - 1
        return df


class Index:
    """Get index data"""

    API_KEY = os.getenv("FRED_API_KEY")

    def __init__(self):
        self.df = self.make_index_df()

    def get_daily_index_prices(self):
        try:
            url = f"https://api.stlouisfed.org/fred/series/observations?series_id=SP500&api_key={Index.API_KEY}&file_type=json"
            r = requests.get(url)
            data = r.json()
            return data
        except:
            raise ValueError

    def make_index_df(self):
        data = self.get_daily_index_prices()
        df = pd.DataFrame(data["observations"])
        df["date"] = pd.to_datetime(df["date"])
        df = (
            df.drop(["realtime_start", "realtime_end"], axis=1)
            .set_index("date")
            .rename(columns={"value": "close"})
        )
        df["close"] = df["close"].apply(pd.to_numeric, errors="coerce")
        df["close_lag_1"] = df["close"].shift(periods=1)
        df["daily_return"] = (df["close"] / df["close_lag_1"]) - 1
        return df
