"""
Lesley Xu
ECON 481

Implements the functions for PS5.
"""

import requests
from bs4 import BeautifulSoup


def github() -> str:
    """
    Takes no arguments and returns a link to my solutions on GitHub.
    """

    return "https://github.com/xlesley/econ-481-problemset/blob/main/ps5.py"


def scrape_code(url: str) -> str:
    """
    Scrape Python code snippets from a lecture webpage and return them as a
    single string.

    Args:
        url (str): The URL of the lecture webpage containing HTML-formatted
        slides with Python code.

    Returns:
        str: A string containing all the Python code snippets extracted from
        the lecture slides. The code snippets are formatted in a way that
        allows saving them as a Python file and running without syntax issues.
        If the webpage fails to fetch, returns None.
    """

    req_obj = requests.get(url)
    if req_obj.status_code == 200:
        soup = BeautifulSoup(req_obj.text)
        code = soup.find_all('code', class_='sourceCode python')
        code_chunk = '\n'.join(item.get_text().strip() for item in code)
        return code_chunk
    else:
        print("Failed to fetch the webpage. Status code:", req_obj.status_code)
        return None
