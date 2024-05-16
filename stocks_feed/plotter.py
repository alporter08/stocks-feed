import matplotlib.pyplot as plt
import seaborn as sns


class Plot:
    def __init__(self):
        pass

    @staticmethod
    def plot_timeseries(x, y, x_label, ylabel, title):
        _, ax = plt.subplots(figsize=(12, 6))

        # Plot the data
        ax.plot(x, y)

        # Set the x-axis label and rotate the tick labels
        ax.set_xlabel(x_label)
        plt.xticks(rotation=45)

        # Set the y-axis label
        ax.set_ylabel(ylabel)

        # Set the plot title
        plt.title(title)

    @staticmethod
    def plot_regression(index_df, stock_df, rsuffix, lsuffix="_SP500"):
        df = index_df.join(stock_df, how="inner", lsuffix=lsuffix, rsuffix=rsuffix)
        sns.lmplot(df, x="daily_return_SP500", y=f"daily_return{rsuffix}")
