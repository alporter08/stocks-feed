import pandas as pd
import statsmodels.api as sm
from stocks_feed.dataloader import Stock, Index


class Risk:
    def __init__(self, stock, index):
        self.stock = stock
        self.index = index

    def concat_series(self):
        stock_returns = self.stock.df["daily_return"]
        index_returns = self.index.df["daily_return"]
        df = pd.concat([stock_returns, index_returns], axis=1).dropna()
        col_names = [self.stock.ticker, self.index.index_name]
        df.columns = col_names
        return df
