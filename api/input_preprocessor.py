import models_loader
import pandas as pd


def preprocess_input_data(dataset: pd.DataFrame) -> pd.DataFrame:
    working_df = dataset.copy()

    encoder = models_loader.load_encoder()
    dataset = encoder.transform(dataset)

    imputer = models_loader.load_imputer()
    dataset = imputer.transform(dataset)

    scaler = models_loader.load_scaler()
    dataset = scaler.transform(dataset)

    return dataset
