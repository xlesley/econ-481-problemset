"""
Lesley Xu
ECON 481

Implements the functions for PS1.
"""

from typing import Union
from datetime import datetime


def github() -> str:
    """
    Takes no arguments and returns a link to my solutions on GitHub.
    """
    return "https://github.com/xlesley/econ-481-problemset/blob/main/ps1.py"


def evens_and_odds(n: int) -> dict[str, int]:
    """
    Takes as argument a natural number n and returns a dictionary with two
    keys, "evens" and "odds". "evens" be the sum of all the even natural
    numbers less than n, and "odds" be the sum of all the odd natural numbers
    less than n.
    """
    evens = 0
    odds = 0
    for i in range(1, n):
        if i % 2 == 0:
            evens += i
        else:
            odds += i
    return {'evens': evens, 'odds': odds}


def time_diff(date_1: str, date_2: str, out: str = 'float') -> Union[str, float]:
    """
    Takes as arguments two strings in the format 'YYYY-MM-DD' and a keyword
    out dictating the output. If the keyword is "float", return the time
    between the two dates (in absolute value) in days. If the keyword is
    "string", return "There are XX days between the two dates".
    If not specified, the out keyword should be assumed to be "float".
    """
    format = "%Y-%m-%d"
    dt1 = datetime.strptime(date_1, format)
    dt2 = datetime.strptime(date_2, format)
    diff = (abs(dt1 - dt2)).days
    if out == 'string':
        return f'There are {diff} days between the two dates'
    return diff


def reverse(in_list: list[str]) -> list[str]:
    """
    Takes as its argument a list and returns a list of the arguments in
    reverse order (do not use any built-in sorting methods).
    """
    return in_list[::-1]


def prob_k_heads(n: int, k: int) -> float:
    """
    Takes as its arguments natural numbers n and k with n > k and returns
    the probability of getting k heads from n flips.
    """
    n_minus_k = 1
    n_choose_k = 1
    for i in range(1, n-k+1):
        n_minus_k *= i
    for i in range(k+1, n+1):
        n_choose_k *= i
    n_choose_k /= n_minus_k
    prob = n_choose_k * (0.5 ** k) * (0.5 ** (n-k))
    return prob
