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


def get_datasets() -> Tuple[pd.DataFrame, pd.DataFrame]:
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

    # Download application_test_aai.csv
    if not os.path.exists(config.DATASET_TEST):
        gdown.download(config.DATASET_TEST_URL, config.DATASET_TEST, quiet=False)

    app_test = pq.read_table(config.DATASET_TEST)
    app_test = app_test.to_pandas()

    return app_train, app_test


def delete_invalid_rows(
    dataset: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
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

    # Validate that empty (NaN) values ​​in multiple columns belong to the same rows
    # Create a new column indicating whether all columns are empty in a specific row
    # Remove rows with multiple empty columns, as they only represents 3% of the dataset

    columns_to_validate = [
        "passenger_count",
        "RatecodeID",
        "store_and_fwd_flag",
        "congestion_surcharge",
        "airport_fee",
    ]
    dataset["empty_columns"] = dataset[columns_to_validate].isnull().all(axis=1)
    dataset = dataset[dataset["empty_columns"] == False]
    return dataset


def get_feature_target(
    app_train_param: pd.DataFrame, app_test_param: pd.DataFrame
) -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
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
    app_train = app_train_param.copy()
    app_test = app_test_param.copy()

    app_train = delete_invalid_rows(app_train)
    app_test = delete_invalid_rows(app_test)

    # Remove rows that are not from 2022
    # it is easy to visualize and analiza training data from the same month
    app_train = app_train[
        (app_train["tpep_pickup_datetime"].dt.year == 2022)
        & (app_train["tpep_dropoff_datetime"].dt.year == 2022)
    ]

    # Remove all rows with trip_distance > 50 because they are outliers in the graphic
    # TODO: check how to achieve it mathematically and not arbitrialy
    app_train = app_train[app_train["trip_distance"] < 50]

    # Remove all rows with RatecodeID > 6 because according to docs RatecodeID can only goes from 1 to 6
    app_train = app_train[app_train["RatecodeID"] < 7]

    # Removing rows with PULocationID > 263 or DOLocationID > 263 because according to the documentation, the maximum value is 265
    # and 264 = Unknown and 265 = NA, they do not add value to the model
    # In total 57190 rows removed
    app_train = app_train[
        (app_train["PULocationID"] < 263) | (app_train["DOLocationID"] < 263)
    ]

    # Replace tpep_pickup_datetime and tpep_dropoff_datetime columns with new columns
    app_train["pickup_day"] = app_train["tpep_pickup_datetime"].dt.day
    app_train["pickup_hour"] = app_train["tpep_pickup_datetime"].dt.hour
    app_train["pickup_minute"] = app_train["tpep_pickup_datetime"].dt.minute
    app_train["dropoff_day"] = app_train["tpep_dropoff_datetime"].dt.day
    app_train["dropoff_hour"] = app_train["tpep_dropoff_datetime"].dt.hour
    app_train["dropoff_minute"] = app_train["tpep_dropoff_datetime"].dt.minute

    # Replace tpep_pickup_datetime and tpep_dropoff_datetime columns with new columns
    app_test["pickup_day"] = app_test["tpep_pickup_datetime"].dt.day
    app_test["pickup_hour"] = app_test["tpep_pickup_datetime"].dt.hour
    app_test["pickup_minute"] = app_test["tpep_pickup_datetime"].dt.minute
    app_test["dropoff_day"] = app_test["tpep_dropoff_datetime"].dt.day
    app_test["dropoff_hour"] = app_test["tpep_dropoff_datetime"].dt.hour
    app_test["dropoff_minute"] = app_test["tpep_dropoff_datetime"].dt.minute

    app_train.drop("tpep_pickup_datetime", inplace=True, axis=1)
    app_train.drop("tpep_dropoff_datetime", inplace=True, axis=1)
    app_train.drop("empty_columns", inplace=True, axis=1)

    app_test.drop("tpep_pickup_datetime", inplace=True, axis=1)
    app_test.drop("tpep_dropoff_datetime", inplace=True, axis=1)

    print(app_train.columns)

    # Assign to X_train all the columns from app_train except "TARGET"
    X_train = app_train.drop("total_amount", axis=1)
    # Assign to y_train the "TARGET" column
    y_train = app_train.total_amount
    # Assign to X_test all the columns from app_test except "TARGET"
    X_test = app_test.drop("total_amount", axis=1)
    # Assign to y_test the "TARGET" column
    y_test = app_test.total_amount

    return X_train, y_train, X_test, y_test


def get_train_val_sets(
    X_train: pd.DataFrame, y_train: pd.Series
) -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
    """
    Split training dataset in two new sets used for train and validation.

    Arguments:
        X_train : pd.DataFrame
            Original training features
        y_train: pd.Series
            Original training labels/target

    Returns:
        X_train : pd.DataFrame
            Training features
        X_val : pd.DataFrame
            Validation features
        y_train : pd.Series
            Training target
        y_val : pd.Series
            Validation target
    """

    X_train, X_val, y_train, y_val = train_test_split(
        X_train,  # independent variables
        y_train,  # dependent variable
        test_size=0.2,
        random_state=42,
        shuffle=True,
    )

    return X_train, X_val, y_train, y_val


# Listado de las features con 2 categorias y otra con mas de dos
def find_columns(X_train: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    #  Encontramos todas las columnas de tipo objeto y contabilizamos sus categorias
    categorias_por_columna = {}
    for columna in X_train.select_dtypes(include=["object"]).columns:
        categorias_por_columna[columna] = X_train[columna].nunique()

    # Inicializar listas para columnas con solo dos categorías y más de dos categorías
    dos_categorias = []
    mas_dos_categorias = []

    # Identificar las columnas con solo dos categorías y más de dos categorías
    for columna, cantidad in categorias_por_columna.items():
        if cantidad == 2:
            dos_categorias.append(columna)
        else:
            mas_dos_categorias.append(columna)

    return dos_categorias, mas_dos_categorias


def transform_data(
    X_train: pd.DataFrame,
    X_val: pd.DataFrame,
    X_test: pd.DataFrame,
    dos_categorias: list,
    mas_dos_categorias: list,
) -> pd.DataFrame:
    # One-hot encoding
    one_hot_encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")

    # Ordinal encoding
    ordinal_encoder = OrdinalEncoder()

    transformers = [
        ("one_hot", one_hot_encoder, mas_dos_categorias),
        ("ordinal", ordinal_encoder, dos_categorias),
    ]

    # Crear el ColumnTransformer
    column_transformer = ColumnTransformer(transformers, remainder="passthrough")

    # Aplicar la transformación a los datos de entrenamiento
    transformer = column_transformer.fit(X_train)

    # Aplicar la transformación a los datos de prueba y validación
    transformed_X_train = transformer.transform(X_train)
    transformed_X_val = transformer.transform(X_val)
    transformed_X_test = transformer.transform(X_test)

    return transformed_X_train, transformed_X_val, transformed_X_test
