from typing import Dict

from pandas import DataFrame
from sqlalchemy.engine.base import Engine


def load(data_frames: Dict[str, DataFrame], database: Engine):
    """Load the dataframes into the sqlite database.

    Args:
        data_frames (Dict[str, DataFrame]): A dictionary with keys as the table names
        and values as the dataframes.
    """
    # TODO: Implement this function. For each dataframe in the dictionary, you must
    # use pandas.Dataframe.to_sql() to load the dataframe into the database as a
    # table.
    # For the table name use the `data_frames` dict keys.
    
    #for key in data_frames:
    #    data_frames[key].to_sql(key, database, if_exists='replace', index= False)

    for table_name, df in data_frames.items():
        df.to_sql(table_name, con=database, if_exists="replace")
        print("done")
    #raise NotImplemetedError