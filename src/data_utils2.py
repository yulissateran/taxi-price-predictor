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
    # Read DATASET_TRAIN_CLEANED
    app_train = pd.read_csv(config.DATASET_TRAIN_CLEANED, delimiter = ",")

    # Download application_test_aai.csv
    #if not os.path.exists(config.DATASET_TEST):
    #    gdown.download(config.DATASET_TEST_URL, config.DATASET_TEST, quiet=False)
    app_test = app_train[:1000]
    #app_test = pd.read_csv(config.DATASET_TEST)

    return app_train, app_test


def get_feature_target(
    app_train: pd.DataFrame, app_test: pd.DataFrame
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

    # TODO

    # Assign to X_train all the columns from app_train except "TARGET"
    X_train = app_train.drop("total_amount", axis=1)
    # Assign to y_train the "TARGET" column
    y_train = app_train.total_amount
    # Assign to X_test all the columns from app_test except "TARGET"
    X_test = app_test.drop("total_amount", axis=1)
    # Assign to y_test the "TARGET" column
    y_test = app_test.total_amount

    return X_train, y_train, X_test, y_test



def get_train_val_sets(X_train: pd.DataFrame, y_train: pd.Series) -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
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
    one_hot_encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')

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

