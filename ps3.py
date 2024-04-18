"""
Lesley Xu
ECON 481

Implements the functions for PS3.
"""

import pandas as pd


def github() -> str:
    """
    Takes no arguments and returns a link to my solutions on GitHub.
    """

    return "https://github.com/xlesley/econ-481-problemset/blob/main/ps3.py"


def import_yearly_data(years: list) -> pd.DataFrame:
    """
    Imports Direct Emitters tab data from EPA Excel sheets for the specified
    years and concatenates them into a single DataFrame.

    Args:
        years (list): A list of years for which data needs to be imported.

    Returns:
        pd.DataFrame: Concatenated DataFrame of Direct Emitters tab data for
        the specified years.
    """
    dfs = []
    for year in years:
        file_path = f"https://lukashager.netlify.app/econ-481/data/ghgp_data_{year}.xlsx"
        df = pd.read_excel(file_path, 'Direct Emitters', header=3)
        df['year'] = year
        dfs.append(df)
    emissions_df = pd.concat(dfs, ignore_index=True)

    return emissions_df


def import_parent_companies(years: list) -> pd.DataFrame:
    """
    Imports data from corresponding tabs in the parent companies Excel sheet
    for the specified years, adds a 'year' column, and concatenates them into
    a single DataFrame.

    Args:
        years (list): A list of years for which data needs to be imported.

    Returns:
        pd.DataFrame: Concatenated DataFrame of data from parent companies
        Excel sheet for the specified years.
    """
    dfs = []
    xls = pd.ExcelFile('https://lukashager.netlify.app/econ-481/data/ghgp_data_parent_company_09_2023.xlsb')
    for year in years:
        df = pd.read_excel(xls, str(year)).dropna(how='all')
        df['year'] = year
        dfs.append(df)
    parent_df = pd.concat(dfs, ignore_index=True)

    return parent_df


def n_null(df: pd.DataFrame, col: str) -> int:
    """
    Counts the number of null values in the specified column of the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing the data.
        col (str): The name of the column for which null values need to be
        counted.

    Returns:
        int: The number of null values in the specified column.
    """
    null_count = df[col].isnull().sum()

    return null_count


def clean_data(emissions_data: pd.DataFrame, parent_data: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the concatenated DataFrame of emissions sheets and parent companies
    data.

    Args:
        emissions_data (pd.DataFrame): Concatenated DataFrame of emissions.
        parent_data (pd.DataFrame): Concatenated DataFrame of parent companies.

    Returns:
        pd.DataFrame: Cleaned DataFrame with specified variables and lowercase
        column names.
    """

    merged_data = pd.merge(emissions_data,
                           parent_data,
                           how='left',
                           left_on=['year', 'Facility Id'],
                           right_on=['year', 'GHGRP FACILITY ID'])

    cleaned_data = merged_data[['Facility Id',
                                'year',
                                'State',
                                'Industry Type (sectors)',
                                'Total reported direct emissions',
                                'PARENT CO. STATE',
                                'PARENT CO. PERCENT OWNERSHIP']]
    cleaned_data.columns = map(str.lower, cleaned_data.columns)

    return cleaned_data


def aggregate_emissions(df: pd.DataFrame, group_vars: list) -> pd.DataFrame:
    """
    Aggregates the specified variables at the level of the variables supplied
    in the group_vars argument.

    Args:
        df (pd.DataFrame): DataFrame with the schema of the output of previous
        exercise.
        group_vars (list): List of variables to group the data by.

    Returns:
        pd.DataFrame: DataFrame with aggregated statistics for the specified
        variables subset.
    """

    agg_df = df.groupby(group_vars, as_index=True).agg({
        'total reported direct emissions': ['min', 'median', 'mean', 'max'],
        'parent co. percent ownership': ['min', 'median', 'mean', 'max']
    })

    agg_df = agg_df.sort_values(by=('total reported direct emissions', 'mean'),
                                ascending=False)

    return agg_df
