from typing import Tuple
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler
from src.data_utils import find_columns, transform_data, delete_invalid_rows
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

    print(type(train_df), type(val_df), type(test_df))
    # Make a copy of the dataframes
    working_train_df = train_df.copy()
    working_val_df = val_df.copy()
    working_test_df = test_df.copy()

    # 1. Correct outliers/anomalous values in
    """     working_train_df = delete_invalid_rows(working_train_df)
    working_val_df = delete_invalid_rows(working_val_df)
    working_test_df = delete_invalid_rows(working_test_df)
    """
    # Remove rows that are not from 2022
    # it is easy to visualize and analiza training data from the same month

    working_train_df.loc[working_train_df["pickup_year"] > 2022, "pickup_year"] = np.nan
    working_val_df.loc[working_val_df["pickup_year"] > 2022, "trip_distance"] = np.nan

    # Replace all rows with trip_distance > 50 because they are outliers in the graphic
    # TODO: check how to achieve it mathematically and not arbitrialy
    working_train_df.loc[working_train_df["trip_distance"] > 50, "trip_distance"] = (
        np.nan
    )
    working_val_df.loc[working_val_df["trip_distance"] > 50, "trip_distance"] = np.nan

    # Remove all rows with RatecodeID > 6 because according to docs RatecodeID can only goes from 1 to 6
    working_train_df.loc[working_train_df["RatecodeID"] > 6, "RatecodeID"] = np.nan
    working_val_df.loc[working_val_df["RatecodeID"] > 6, "RatecodeID"] = np.nan

    # Removing rows with PULocationID > 263 or DOLocationID > 263 because according to the documentation, the maximum value is 265
    # and 264 = Unknown and 265 = NA, they do not add value to the model
    # In total 57190 rows removed
    working_train_df.loc[working_train_df["PULocationID"] > 263, "PULocationID"] = (
        np.nan
    )
    working_train_df.loc[working_train_df["DOLocationID"] > 263, "DOLocationID"] = (
        np.nan
    )

    working_val_df.loc[working_val_df["PULocationID"] > 263, "PULocationID"] = np.nan
    working_val_df.loc[working_val_df["DOLocationID"] > 263, "DOLocationID"] = np.nan

    # Replacing None values in store_and_fwd_flag with 'N'
    working_val_df["store_and_fwd_flag"].replace({None: "N"}, inplace=True)
    working_val_df["store_and_fwd_flag"].replace({None: "N"}, inplace=True)
    working_test_df["store_and_fwd_flag"].replace({None: "N"}, inplace=True)
    # 2.  - If the feature has 2 categories encode using binary encoding,
    #       please use `sklearn.preprocessing.OrdinalEncoder()`. Only 4 columns
    #       from the dataset should have 2 categories.
    #     - If it has more than 2 categories, use one-hot encoding, please use
    #       `sklearn.preprocessing.OneHotEncoder()`. 12 columns
    #       from the dataset should have more than 2 categories.

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
