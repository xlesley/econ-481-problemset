"""
Lesley Xu
ECON 481

Implements the functions for PS2.
"""

import numpy as np
import scipy as sp


def github() -> str:
    """
    Takes no arguments and returns a link to my solutions on GitHub.
    """

    return "https://github.com/xlesley/econ-481-problemset/blob/main/ps2.py"


def simulate_data(seed: int = 481) -> tuple:
    """
    Simulates data for a linear regression model.

    Args:
        seed (int, optional): Seed for the random number generator.
        Defaults to 481.

    Returns:
        tuple: A tuple containing y and X, where y is a numpy array of shape
               (1000, 1) representing the response variable, and X is a numpy
               array of shape (1000, 3) representing the predictor variables.
    """
    np.random.seed(seed)
    X = np.random.normal(loc=0, scale=np.sqrt(2), size=(1000, 3))
    epsilon = np.random.normal(loc=0, scale=1, size=1000)
    y = (5 + 3 * X[:, 0] + 2 * X[:, 1] + 6 * X[:, 2] + epsilon)
    return (y.reshape((-1, 1)), X)


def neg_ll(beta: np.array, y: np.array, X: np.array) -> np.array:
    """
    Calculates the negative log-likelihood for a linear regression model.

    Args:
        beta (np.array): Coefficients of the linear regression model.
        y (np.array): Response variable values.
        X (np.array): Predictor variable values.

    Returns:
        np.array: Negative log-likelihood value.
    """
    n = len(y)
    epsilon = y - (beta[0] + X @ beta[1:]).reshape(-1, 1)
    variance = 1
    log_likelihood = -n / 2 * np.log(2 * np.pi * variance) \
        - 1 / (2 * variance) * np.sum(epsilon ** 2)
    return -log_likelihood


def estimate_mle(y: np.array, X: np.array) -> np.array:
    """
    Estimates the maximum likelihood coefficients for a linear regression
    model.

    Args:
        y (np.array): Response variable values.
        X (np.array): Predictor variable values.

    Returns:
        np.array: Coefficients estimated using maximum likelihood estimation.
    """
    initial_guess = np.zeros(4)
    betas = sp.optimize.minimize(fun=neg_ll,
                                 x0=initial_guess,
                                 args=(y, X),
                                 method='Nelder-Mead').x
    return betas.reshape((-1, 1))


def rss(beta: np.array, y: np.array, X: np.array) -> np.array:
    """
    Calculates the sum of squared residuals for a linear regression model.

    Args:
        beta (np.array): Coefficients of the linear regression model.
        y (np.array): Response variable values.
        X (np.array): Predictor variable values.

    Returns:
        np.array: Sum of squared residuals.
    """
    y_hat = (beta[0] + X @ beta[1:]).reshape(-1, 1)
    residual = y - y_hat
    val = np.sum(residual ** 2)
    return val


def estimate_ols(y: np.array, X: np.array) -> np.array:
    """
    Estimates the coefficients for a linear regression model using OLS.

    Args:
        y (np.array): Response variable values.
        X (np.array): Predictor variable values.

    Returns:
        np.array: Coefficients estimated using ordinary least squares.
    """
    initial_guess = np.zeros(4)
    betas = sp.optimize.minimize(fun=rss,
                                 x0=initial_guess,
                                 args=(y, X)).x
    return betas.reshape((-1, 1))
