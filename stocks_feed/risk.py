import pandas as pd
import statsmodels.api as sm
from stocks_feed.dataloader import Stock, Index


class Risk:
    def __init__(self, stock, index):
        self.stock = stock
        self.index = index
        self.ols_results = self.ols()

    def concat_series(self):
        stock_returns = self.stock.df["daily_return"]
        index_returns = self.index.df["daily_return"]
        df = pd.concat([stock_returns, index_returns], axis=1).dropna()
        col_names = [self.stock.ticker, self.index.index_name]
        df.columns = col_names
        return df

    def ols(self):
        df = self.concat_series()
        y = df[self.stock.ticker]
        X = df[self.index.index_name]
        X = sm.add_constant(X)
        results = sm.OLS(y, X).fit()
        return results

    def ols_summary(self):
        print(self.ols_results.summary())
