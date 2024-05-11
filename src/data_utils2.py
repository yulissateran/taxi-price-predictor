import os
from typing import Tuple
import pyarrow.parquet as pq

import gdown
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from src import config


def get_datasets() -> Tuple[pd.DataFrame]:
    """
    Download from GDrive all the needed datasets for the project.

    Returns:
        app_train : pd.DataFrame
            Training dataset

        app_test : pd.DataFrame
            Test dataset

        columns_description : pd.DataFrame
            Extra dataframe with detailed description about dataset features
    """
    # Download application_train_aai.csv

    if not os.path.exists(config.DATASET_TRAIN):
        gdown.download(config.DATASET_TRAIN_URL, config.DATASET_TRAIN, quiet=False)

    app_train = pq.read_table(config.DATASET_TRAIN)
    app_train = app_train.to_pandas()

    return app_train


def get_feature_target(app_train: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Separates our train and test datasets columns between Features
    (the input to the model) and Targets (what the model has to predict with the
    given features).

    Arguments:
        app_train : pd.DataFrame
            Training datasets
        app_test : pd.DataFrame
            Test datasets

    Returns:
        X_train : pd.DataFrame
            Training features
        y_train : pd.Series
            Training target
        X_test : pd.DataFrame
            Test features
        y_test : pd.Series
            Test target
    """

    # TODO

    # Assign to X_train all the columns from app_train except "TARGET"
    X_train = app_train.drop("total_amount", axis=1)
    # Assign to y_train the "TARGET" column
    y_train = app_train.total_amount

    return X_train, y_train
