from typing import Tuple
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler
from src.data_utils import find_columns, transform_data
from joblib import dump, load
from src.save_model import save_encoder, save_imputer, save_scaler


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

    dos_categorias, mas_dos_categorias = find_columns(working_train_df)
    transformed_train, Tranformed_X_val, Transformed_X_test, transformer = (
        transform_data(
            working_train_df,
            working_val_df,
            working_test_df,
            dos_categorias,
            mas_dos_categorias,
        )
    )
    save_encoder(transformer)

    # Crear un imputador con estrategia de imputación de mediana
    # Ajustar el imputador solo en el conjunto de datos de entrenamiento
    imputer = SimpleImputer(strategy="median")
    imp = imputer.fit(transformed_train)
    save_imputer(imp)

    # Transformar todos los conjuntos de datos utilizando el imputador ajustado
    imputed_train_df = imp.transform(transformed_train)
    imputed_val_df = imp.transform(Tranformed_X_val)
    imputed_test_df = imp.transform(Transformed_X_test)

    # Feature scaling with Min-Max scaler. Apply this to all the columns.
    # Ajustar el scaler solo en el conjunto de datos de entrenamiento
    scaler = MinMaxScaler()
    scaler = scaler.fit(imputed_train_df)
    save_scaler(scaler)

    # Transformar todos los conjuntos de datos utilizando el scaler ajustado
    scaled_train_df = scaler.transform(imputed_train_df)
    scaled_val_df = scaler.transform(imputed_val_df)
    scaled_test_df = scaler.transform(imputed_test_df)

    return scaled_train_df, scaled_val_df, scaled_test_df
