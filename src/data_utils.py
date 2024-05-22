import os
from typing import Tuple
import pyarrow.parquet as pq

import gdown
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import numpy as np
#from data_utils import agregate_columns

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

        # 1. Correct outliers/anomalous values in the dataset.
    # passengers number should be between 1 and 6 according documentation
    # Se encontraron valores entre 0 y 8,
    # 0 valores sin pasajeros para entrega de paquetes
    # mas de 6 segun tipo de transporte.
    #app_train.loc[app_train["passenger_count"] > 6, "passenger_count"] = (
    #    np.nan
    #)
    #app_test.loc[app_test["passenger_count"] > 6, "passenger_count"] = np.nan


    #app_train.loc[app_train["passenger_count"] < 1, "passenger_count"] = (
    #    np.nan
    #)
    #app_test.loc[app_test["passenger_count"] < 1, "passenger_count"] = (
    #    np.nan
    #)
    # TODO: check how to achieve it mathematically using IQR and not arbitrialy

    # visually saw on the histplot that most of the rows are under 100



    # Se uso 3 desviaciones estandar para el filtrado de los dos dataset train y val. Usar grafico para mostrar cambios.
    mean_train = app_train['fare_amount'].mean()
    std_train = app_train['fare_amount'].std()

    app_train['fare_amount_sigmas'] = (app_train['fare_amount'] - mean_train) / std_train

    app_train = app_train[
        (app_train['fare_amount_sigmas'] < 3) &
        (app_train['fare_amount_sigmas'] > -3)
    ]

    app_train = app_train[app_train['fare_amount']>0]
    app_train.drop("fare_amount_sigmas", inplace=True, axis=1)
    

    mean_test = app_test['fare_amount'].mean()
    std_val = app_test['fare_amount'].std()

    app_test['fare_amount_sigmas'] = (app_test['fare_amount'] - mean_test) / std_val

    app_test = app_test[
        (app_test['fare_amount_sigmas'] < 3) &
        (app_test['fare_amount_sigmas'] > -3)
    ]

    app_test = app_test[app_test['fare_amount']>0]
    app_test.drop("fare_amount_sigmas", inplace=True, axis=1)

 #   app_train.loc[app_train["fare_amount"] <= 1, "fare_amount"] = np.nan
 #   app_test.loc[app_test["fare_amount"] <= 1, "fare_amount"] = np.nan
 #   app_train.loc[app_train["fare_amount"] >= 100, "fare_amount"] = np.nan
 #   app_test.loc[app_test["fare_amount"] >= 100, "fare_amount"] = np.nan

    app_train =  agregate_columns(app_train)
    app_test =  agregate_columns(app_test)


    # Remove rows that are not from 2022
    # it is easy to visualize and analiza training data from the same month
    app_train.loc[app_train["pickup_year"] != 2022, "pickup_year"] = np.nan
    app_test.loc[app_test["pickup_year"] != 2022, "pickup_year"] = np.nan

    # Replace all rows with trip_distance > 50 because they are outliers in the graphic
    # TODO: check how to achieve it mathematically and not arbitrialy
    app_train.loc[app_train["trip_distance"] > 60, "trip_distance"] = (
        np.nan
    )
    app_test.loc[app_test["trip_distance"] > 60, "trip_distance"] = np.nan   

    # Remove all rows with RatecodeID > 6 because according to docs RatecodeID can only goes from 1 to 6
    app_train.loc[app_train["RatecodeID"] > 6, "RatecodeID"] = np.nan
    app_test.loc[app_test["RatecodeID"] > 6, "RatecodeID"] = np.nan

    # Removing rows with PULocationID > 263 or DOLocationID > 263 because according to the documentation, the maximum value is 265
    # and 264 = Unknown and 265 = NA, they do not add value to the model
    # In total 57190 rows removed
    app_train.loc[app_train["PULocationID"] > 263, "PULocationID"] = (
        np.nan
    )
    app_test.loc[app_test["DOLocationID"] > 263, "DOLocationID"] = (
        np.nan
    )

    app_train = app_train[app_train['total_amount']<400]
    app_test = app_test[app_test['total_amount']<400]


    #app_test.loc[app_test["PULocationID"] > 263, "PULocationID"] = np.nan
    #app_test.loc[app_test["DOLocationID"] > 263, "DOLocationID"] = np.nan

    # Replacing None values in store_and_fwd_flag with 'N'
    app_test["store_and_fwd_flag"].replace({None: "N"}, inplace=True)
    app_train["store_and_fwd_flag"].replace({None: "N"}, inplace=True)
    #app_test["store_and_fwd_flag"].replace({None: "N"}, inplace=True)
    # 2.  - If the feature has 2 categories encode using binary encoding,
    #       please use `sklearn.preprocessing.OrdinalEncoder()`. Only 4 columns
    #       from the dataset should have 2 categories.
    #     - If it has more than 2 categories, use one-hot encoding, please use
    #       `sklearn.preprocessing.OneHotEncoder()`. 12 columns
    #       from the dataset should have more than 2 categories.

    # Removing columns that are not available in the momment that users are going to predict total amount and duration
    app_test.drop("fare_amount", inplace=True, axis=1)
    app_train.drop("fare_amount", inplace=True, axis=1)
    #app_test.drop("fare_amount", inplace=True, axis=1)

    app_test.drop("store_and_fwd_flag", inplace=True, axis=1)
    app_train.drop("store_and_fwd_flag", inplace=True, axis=1)
    #app_test.drop("store_and_fwd_flag", inplace=True, axis=1)

    app_test.drop("trip_distance", inplace=True, axis=1)
    app_train.drop("trip_distance", inplace=True, axis=1)
    #app_test.drop("trip_distance", inplace=True, axis=1)

    app_test.drop("RatecodeID", inplace=True, axis=1)
    app_train.drop("RatecodeID", inplace=True, axis=1)
    #app_test.drop("RatecodeID", inplace=True, axis=1)

    app_test.drop("VendorID", inplace=True, axis=1)
    app_train.drop("VendorID", inplace=True, axis=1)
    #app_test.drop("VendorID", inplace=True, axis=1)

    app_test.drop("tolls_amount", inplace=True, axis=1)
    app_train.drop("tolls_amount", inplace=True, axis=1)
    #app_test.drop("tolls_amount", inplace=True, axis=1)

    app_test.drop("congestion_surcharge", inplace=True, axis=1)
    app_train.drop("congestion_surcharge", inplace=True, axis=1)
    #app_test.drop("congestion_surcharge", inplace=True, axis=1)

    app_test.drop("tip_amount", inplace=True, axis=1)
    app_train.drop("tip_amount", inplace=True, axis=1)
    #app_test.drop("tip_amount", inplace=True, axis=1)

    app_test.drop("mta_tax", inplace=True, axis=1)
    app_train.drop("mta_tax", inplace=True, axis=1)
    #app_test.drop("mta_tax", inplace=True, axis=1)

    app_test.drop("extra", inplace=True, axis=1)
    app_train.drop("extra", inplace=True, axis=1)
    #app_test.drop("extra", inplace=True, axis=1)

    print("columns", app_test.columns)

    return app_train, app_test


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
    dataset["pickup_day_of_week"] = dataset["tpep_pickup_datetime"].dt.dayofweek
    dataset["pickup_hour"] = dataset["tpep_pickup_datetime"].dt.hour
    dataset["pickup_minute"] = dataset["tpep_pickup_datetime"].dt.minute

    dataset.drop("tpep_pickup_datetime", inplace=True, axis=1)
    dataset.drop("tpep_dropoff_datetime", inplace=True, axis=1)





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
