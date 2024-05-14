from typing import Tuple

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler

from src.data_utils import find_columns, transform_data


def preprocess_data(
    train_df: pd.DataFrame, val_df: pd.DataFrame, test_df: pd.DataFrame
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Pre processes data for modeling. Receives train, val and test dataframes
    and returns numpy ndarrays of cleaned up dataframes with feature engineering
    already performed.

    Arguments:
        train_df : pd.DataFrame
        val_df : pd.DataFrame
        test_df : pd.DataFrame

    Returns:
        train : np.ndarrary
        val : np.ndarrary
        test : np.ndarrary
    """
    # Print shape of input data
    print("Input train data shape: ", train_df.shape)
    print("Input val data shape: ", val_df.shape)
    print("Input test data shape: ", test_df.shape, "\n")

    # Make a copy of the dataframes
    working_train_df = train_df.copy()
    working_val_df = val_df.copy()
    working_test_df = test_df.copy()

    # 1. Correct outliers/anomalous values in
    # 2.  - If the feature has 2 categories encode using binary encoding,
    #       please use `sklearn.preprocessing.OrdinalEncoder()`. Only 4 columns
    #       from the dataset should have 2 categories.
    #     - If it has more than 2 categories, use one-hot encoding, please use
    #       `sklearn.preprocessing.OneHotEncoder()`. 12 columns
    #       from the dataset should have more than 2 categories.

    dos_categorias, mas_dos_categorias = find_columns(working_train_df)

    transformed_train, Tranformed_X_val, Transformed_X_test = transform_data(
        working_train_df,
        working_val_df,
        working_test_df,
        dos_categorias,
        mas_dos_categorias,
    )

    # Crear un imputador con estrategia de imputación de mediana
    imputer = SimpleImputer(strategy="median")

    # Ajustar el imputador solo en el conjunto de datos de entrenamiento
    imp = imputer.fit(transformed_train)

    # Transformar todos los conjuntos de datos utilizando el imputador ajustado
    imputed_train_df = imp.transform(transformed_train)
    imputed_val_df = imp.transform(Tranformed_X_val)
    imputed_test_df = imp.transform(Transformed_X_test)

    # Feature scaling with Min-Max scaler. Apply this to all the columns.

    scaler = MinMaxScaler()
    # Ajustar el scaler solo en el conjunto de datos de entrenamiento
    scaler.fit(imputed_train_df)

    # Transformar todos los conjuntos de datos utilizando el scaler ajustado
    scaled_train_df = scaler.transform(imputed_train_df)
    scaled_val_df = scaler.transform(imputed_val_df)
    scaled_test_df = scaler.transform(imputed_test_df)

    return scaled_train_df, scaled_val_df, scaled_test_df
