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


def agregate_columns_to_input(
    dataset: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
    # Replace tpep_pickup_datetime and tpep_dropoff_datetime columns with new columns
    dataset["pickup_year"] = dataset["tpep_pickup_datetime"].dt.year
    dataset["pickup_day"] = dataset["tpep_pickup_datetime"].dt.day
    dataset["pickup_hour"] = dataset["tpep_pickup_datetime"].dt.hour
    dataset["pickup_minute"] = dataset["tpep_pickup_datetime"].dt.minute

    dataset.drop("tpep_pickup_datetime", inplace=True, axis=1)
    return dataset


def agregate_columns(
    dataset: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:

    # Add the new 'duration_in_minutes' column to the DataFrame
    dataset["duration_in_minutes"] = (
        dataset["tpep_dropoff_datetime"] - dataset["tpep_pickup_datetime"]
    ).dt.total_seconds() / 60

    # Replace tpep_pickup_datetime and tpep_dropoff_datetime columns with new columns
    dataset["pickup_year"] = dataset["tpep_pickup_datetime"].dt.year
    dataset["pickup_day"] = dataset["tpep_pickup_datetime"].dt.day
    dataset["pickup_hour"] = dataset["tpep_pickup_datetime"].dt.hour
    dataset["pickup_minute"] = dataset["tpep_pickup_datetime"].dt.minute

    dataset.drop("tpep_pickup_datetime", inplace=True, axis=1)
    dataset.drop("tpep_dropoff_datetime", inplace=True, axis=1)
    return dataset


def delete_invalid_rows(
    dataset: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
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
    X_train = app_train_param.copy()
    X_test = app_test_param.copy()

    # Assign to y_train the "TARGET" column
    y_train_total_amount = X_train.total_amount
    y_train_duration_in_minutes = X_train.duration_in_minutes

    # Assign to X_train all the columns from app_train except "TARGET"
    X_train.drop("total_amount", inplace=True, axis=1)
    X_train.drop("duration_in_minutes", inplace=True, axis=1)

    # X_train = X_train.drop("total_amount", axis=1)
    # X_train = X_train.drop("duration_in_minutes", axis=1)

    # Assign to y_test the "TARGET" column
    y_test_total_amount = X_test.total_amount
    y_test_duration_in_minutes = X_test.duration_in_minutes

    # Assign to X_test all the columns from app_test except "TARGET"
    X_test.drop("total_amount", inplace=True, axis=1)
    X_test.drop("duration_in_minutes", inplace=True, axis=1)

    return (
        X_train,
        y_train_total_amount,
        y_train_duration_in_minutes,
        X_test,
        y_test_total_amount,
        y_test_duration_in_minutes,
    )


def get_train_val_sets(
    X_train: pd.DataFrame,
    y_train_total_amount: pd.Series,
    y_train_duration_in_minutes: pd.Series,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series, pd.Series, pd.Series]:
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

    (
        X_train,
        X_val,
        y_train_total_amount,
        y_val_total_amount,
        y_train_duration_in_minutes,
        y_val_duration_in_minutes,
    ) = train_test_split(
        X_train,
        y_train_total_amount,
        y_train_duration_in_minutes,
        test_size=0.2,
        random_state=42,
        shuffle=True,
    )

    return (
        X_train,
        X_val,
        y_train_total_amount,
        y_val_total_amount,
        y_train_duration_in_minutes,
        y_val_duration_in_minutes,
    )


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
    # Ordinal encoding
    one_hot_encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
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

    return transformed_X_train, transformed_X_val, transformed_X_test, transformer
