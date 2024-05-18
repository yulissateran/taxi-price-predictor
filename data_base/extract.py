from typing import Dict

import pyarrow.parquet as pq
from pandas import DataFrame, read_csv

def read_parquet(filepath: str) -> DataFrame:
    """Reads a Parquet file and returns a Pandas DataFrame.

    Args:
        filepath (str): The path to the Parquet file.

    Returns:
        DataFrame: The Pandas DataFrame containing the data from the Parquet file.
    """

    table = pq.read_table(filepath)
    return table.to_pandas()  # Convert PyArrow Table to Pandas DataFrame

def extract(
    parquet_folder: str, parquet_table_mapping: Dict[str, str]
) -> Dict[str, DataFrame]:
    """Extract the data from the parquet files and load them into the dataframes.
    Args:
        csv_folder (str): The path to the csv's folder.
        csv_table_mapping (Dict[str, str]): The mapping of the csv file names to the
        table names.
        public_holidays_url (str): The url to the public holidays.
    Returns:
        Dict[str, DataFrame]: A dictionary with keys as the table names and values as
        the dataframes.
    """
    dataframes = {
        table_name: read_parquet(f"{parquet_folder}/{parquet_file}")  # Use read_parquet
        for parquet_file, table_name in parquet_table_mapping.items()
    }



    return dataframes
