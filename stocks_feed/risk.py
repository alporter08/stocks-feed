import numpy as np
import pandas as pd
import statsmodels.api as sm
from stocks_feed.dataloader import Stock, Index


class Risk:
    def __init__(self, stock, index, nmv=10_000_000):
        self.stock = stock
        self.index = index
        self.ols_results, self.X, self.y = self.ols()
        self.risk_params = self.get_risk_params()
        self.single_stock_vols = self.get_single_stock_vol(nmv)

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
        return results, X, y

    def ols_summary(self):
        print(self.ols_results.summary())

    def get_risk_params(self):
        alpha = self.ols_results.params["const"]
        beta = self.ols_results.params[self.index.index_name]
        daily_mkt_vol_perc = np.std(self.X[self.index.index_name]) * 100
        daily_idio_vol_perc = (
            np.std(self.y - (alpha + beta * self.X[self.index.index_name])) * 100
        )
        risk_params = {
            "alpha": alpha,
            "beta": beta,
            "daily_mkt_vol_perc": daily_mkt_vol_perc,
            "daily_idio_vol_perc": daily_idio_vol_perc,
        }
        return risk_params

    def get_single_stock_vol(self, nmv=10_000_000):
        market_vol = (
            self.risk_params["beta"]
            * self.risk_params["daily_mkt_vol_perc"]
            * nmv
            / 100
        )
        idio_vol = self.risk_params["daily_idio_vol_perc"] * nmv / 100
        total_vol = np.sqrt(market_vol**2 + idio_vol**2)
        vols = {"market_vol": market_vol, "idio_vol": idio_vol, "total_vol": total_vol}
        return vols
