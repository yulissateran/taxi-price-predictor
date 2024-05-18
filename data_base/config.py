from pathlib import Path
from typing import Dict


DATASET_ROOT_PATH = str(Path(__file__).parent.parent / "dataset")
SQLITE_BD_ABSOLUTE_PATH = str(Path(__file__).parent.parent / "taxi_price_p.db")
PUBLIC_TRIP_RECORDS_MAY2022_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-05.parquet"

def get_parquet_to_table_mapping() -> Dict[str, str]:
    """This function maps the csv files to the table names.

    Returns:
        Dict[str, str]: Dictionary with keys as the csv file names and
        values as the table names.
    """
    return dict(
        [
            ("trans_data_TEST.parquet", "trans_data_TEST"),
            ("trans_data.parquet", "trans_data"),
        ]
    )