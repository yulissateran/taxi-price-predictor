import pandas as pd


def agregate_columns_to_input(
    dataset: pd.DataFrame,
):
    # Replace tpep_pickup_datetime and tpep_dropoff_datetime columns with new columns
    dataset["pickup_year"] = dataset["tpep_pickup_datetime"].dt.year
    dataset["pickup_day"] = dataset["tpep_pickup_datetime"].dt.day
    dataset["pickup_hour"] = dataset["tpep_pickup_datetime"].dt.hour
    dataset["pickup_minute"] = dataset["tpep_pickup_datetime"].dt.minute

    dataset.drop("tpep_pickup_datetime", inplace=True, axis=1)
    return dataset
