import numpy as np
import pandas as pd
import statsmodels.api as sm


class Risk:
    """Computes various risk metrics for a stock.

    The class performs OLS regression on a Stock and Index to obtain estimates for
    alpha, beta and epsilon based on the equation r = alpha + beta * m + eps.

    Attributes:
        stock: A Stock object that contains a ticker, a start date, end date and
        dataframe of daily returns.
        index: An Index object that contains an index_name and a dataframe of daily
        returns.
        ols_results: statsmodels.regression.linear_model.RegressionResultsWrapper
        X: Daily index returns with constant for regression.
        y: Daily stock returns with constant for regression.
        risk_params: Dictionary containing alpha, beta, daily market volatility (%)
        and daily idiosyncratic volatility (%)
        single_stock_vols: Market volatility, Idiosyncratic volatility and Total
        volatility components for a position of X Net Market Value.
    """

    def __init__(self, stock, index, nmv=10_000_000):
        """Initializes the instance based on the stock and the index.
        Defaults to a Net Market Value of $10m for the volatility
        calculations.

        Args:
          stock: The stock on which the risk analysis will be performed.
          index: The benchmark index.
          nmv: The Net Market Value of the the asset.
        """
        self.stock = stock
        self.index = index
        self.ols_results, self.X, self.y = self.ols()
        self.risk_params = self.get_risk_params()
        self.single_stock_vols = self.get_single_stock_vol(nmv)

    def concat_series(self):
        """Returns a dataframe consisting of stock and index dataframes."""
        stock_returns = self.stock.df["daily_return"]
        index_returns = self.index.df["daily_return"]
        df = pd.concat([stock_returns, index_returns], axis=1).dropna()
        col_names = [self.stock.ticker, self.index.index_name]
        df.columns = col_names
        return df

    def ols(self):
        """Performs OLS regression on stock and index and returns OLS results object
        along with X and y series."""
        df = self.concat_series()
        y = df[self.stock.ticker]
        X = df[self.index.index_name]
        X = sm.add_constant(X)
        results = sm.OLS(y, X).fit()
        return results, X, y

    def ols_summary(self):
        """Prints the OLS results summary."""
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
