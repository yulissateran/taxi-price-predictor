import joblib
from src import config


def save_duration_trip_model(model):
    path = f"{config.MODELS_ROOT_PATH}/duration_trip.pkl"
    joblib.dump(model, path)


def save_total_trip_model(model):
    path = f"{config.MODELS_ROOT_PATH}/total_trip.pkl"
    joblib.dump(model, path)


def save_encoder(model):
    path = f"{config.ENCODERS_ROOT_PATH}/encoder.joblib"
    joblib.dump(model, path)


def save_imputer(model):
    path = f"{config.ENCODERS_ROOT_PATH}/imputer.joblib"
    joblib.dump(model, path)


def save_scaler(model):
    path = f"{config.ENCODERS_ROOT_PATH}/scaler.joblib"
    joblib.dump(model, path)
