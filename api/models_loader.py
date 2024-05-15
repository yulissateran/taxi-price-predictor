import joblib
import config


def load_duration_trip_model():
    path = f"{config.MODELS_ROOT_PATH}/duration_trip.pkl"
    model = joblib.load(path)
    return model


def load_total_trip_model():
    path = f"{config.MODELS_ROOT_PATH}/total_trip.pkl"
    model = joblib.load(path)
    return model


def load_encoder():
    path = f"{config.ENCODERS_ROOT_PATH}/encoder.joblib"
    model = joblib.load(path)
    return model


def load_imputer():
    path = f"{config.ENCODERS_ROOT_PATH}/imputer.joblib"
    model = joblib.load(path)
    return model


def load_scaler():
    path = f"{config.ENCODERS_ROOT_PATH}/scaler.joblib"
    model = joblib.load(path)
    return model
