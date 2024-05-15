import os
from pathlib import Path

DATASET_ROOT_PATH = str(Path(__file__).parent.parent / "api" / "dataset")
MODELS_ROOT_PATH = str(Path(__file__).parent.parent / "api" / "models")
ENCODERS_ROOT_PATH = str(Path(__file__).parent.parent / "api" / "encoders")

os.makedirs(DATASET_ROOT_PATH, exist_ok=True)
os.makedirs(MODELS_ROOT_PATH, exist_ok=True)
os.makedirs(ENCODERS_ROOT_PATH, exist_ok=True)

DATASET_TRAIN = str(Path(DATASET_ROOT_PATH) / "trans_data.parquet")
DATASET_TRAIN_URL = (
    "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-05.parquet"
)

DATASET_TRAIN_CLEANED = str(
    Path(DATASET_ROOT_PATH) / "trans_data_ready_to_feature_eng.csv"
)

DATASET_TEST = str(Path(DATASET_ROOT_PATH) / "trans_data_TEST.parquet")
DATASET_TEST_URL = (
    "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-06.parquet"
)
