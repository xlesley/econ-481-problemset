"""
Lesley Xu
ECON 481

Implements the functions for PS4.
"""

import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf


def github() -> str:
    """
    Takes no arguments and returns a link to my solutions on GitHub.
    """

    return "https://github.com/xlesley/econ-481-problemset/blob/main/ps4.py"


def load_data() -> pd.DataFrame:
    """
    Load Tesla stock price history data from the course website.

    Returns:
        pd.DataFrame: DataFrame containing Tesla stock price history.
    """

    df = pd.read_csv('https://lukashager.netlify.app/econ-481/data/TSLA.csv')

    return df


def plot_close(df: pd.DataFrame, start: str = '2010-06-29',
               end: str = '2024-04-15') -> None:
    """
    Plot the closing price of a DataFrame within a specified date range.

    Args:
        df (pd.DataFrame): DataFrame containing 'Date' and 'Close' columns.
        start (str, optional): Start date of the plot in 'YYYY-MM-DD' format. Default is '2010-06-29'.
        end (str, optional): End date of the plot in 'YYYY-MM-DD' format. Default is '2024-04-15'.

    Returns:
        None
    """

    df['Date'] = pd.to_datetime(df['Date'])
    plot_df = df[(df['Date'] >= start) & (df['Date'] <= end)]

    plt.figure(figsize=(10, 6))
    plt.xlabel('Date')
    plt.xticks(rotation=45)
    plt.ylabel('Close')
    plt.plot(plot_df['Date'], plot_df['Close'])
    plt.title(f'Closing price from {start} to {end}')
    plt.show()


def autoregress(df: pd.DataFrame) -> float:
    """
    Compute the t statistic for the lagged change in close price using
    autoregression. HC1 standard errors are used for the regression.

    Args:
        df (pd.DataFrame): DataFrame containing 'Date' and 'Close' columns.

    Returns:
        float: t statistic on the coefficient of the lagged change in close price.
    """

    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date')
    df['Close_Lag'] = df['Close'].shift(1, freq="D")
    df['delta_t'] = df['Close'] - df['Close_Lag']
    df['delta_lag'] = df['delta_t'].shift(1, freq="D")
    df.dropna(inplace=True)

    model = smf.ols('delta_t ~ delta_lag -1', data=df).fit(cov_type='HC1')

    return model.tvalues['delta_lag']


def autoregress_logit(df: pd.DataFrame) -> float:
    """
    Compute the t-statistic from logistic regression.

    Args:
        df (pd.DataFrame): DataFrame containing 'Date' and 'Close' columns.

    Returns:
        float: t-statistic of the coefficient in the logistic regression.
    """

    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date')
    df['Close_Lag'] = df['Close'].shift(1, freq="D")
    df['delta_t'] = df['Close'] - df['Close_Lag']
    df['delta_lag'] = df['delta_t'].shift(1, freq="D")
    df['delta_positive'] = (df['delta_t'] > 0).astype(int)
    df.dropna(inplace=True)

    model = smf.logit('delta_positive ~ delta_lag - 1', data=df).fit()

    return model.tvalues['delta_lag']


def plot_delta(df: pd.DataFrame) -> None:
    """
    Plot the trend of delta_t.

    Args:
        df (pd.DataFrame): DataFrame containing 'Date' and 'Close' columns.

    Returns:
        None
    """

    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date')
    df['Close_Lag'] = df['Close'].shift(1, freq="D")
    df['delta_t'] = df['Close'] - df['Close_Lag']
    df.dropna(inplace=True)
    df.reset_index(inplace=True)

    plt.figure(figsize=(10, 6))
    plt.xlabel('Date')
    plt.xticks(rotation=45)
    plt.ylabel('$\\Delta x_{{t}}$')
    plt.plot(df['Date'], df['delta_t'])
    plt.title('$\\Delta x_{{t}}$ for the full dataset')
    plt.show()
