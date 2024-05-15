from flask import (
    Blueprint,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)

import joblib
import models_loader, input_preprocessor, agregate_columns
from datetime import datetime
import pandas as pd

router = Blueprint("app_router", __name__)
total_trip_model = models_loader.load_total_trip_model()
duration_trip_model = models_loader.load_duration_trip_model()


@router.route("/predict", methods=["POST"])
def predict():
    """
    POST: Used in our frontend so we can upload and show an image.
    When it receives an image from the UI, it also calls our ML model to
    get and display the predictions.
    """

    # data = request.get_json()
    data = {}
    data["fare_amount"] = 17.0
    data["VendorID"] = 1
    data["store_and_fwd_flag"] = "N"

    data["tpep_pickup_datetime"] = datetime.strptime(
        "2022-05-01 00:00:36", "%Y-%m-%d %H:%M:%S"
    )
    #  data["tpep_dropoff_datetime"] = datetime.strptime(
    #      "2022-05-01 00:19:18", "%Y-%m-%d %H:%M:%S"
    # )

    # total_amount: 20.80
    data["passenger_count"] = 1.0
    data["trip_distance"] = 4.1
    data["RatecodeID"] = 1.0
    data["PULocationID"] = 246
    data["DOLocationID"] = 151
    data["payment_type"] = 2
    data["extra"] = 3.0
    data["mta_tax"] = 0.5
    data["tip_amount"] = 0.00
    data["tolls_amount"] = 0.0
    data["improvement_surcharge"] = 0.3
    data["congestion_surcharge"] = 2.5
    data["airport_fee"] = 0.0
    df = pd.DataFrame(data, index=[0])
    df = agregate_columns.agregate_columns_to_input(df)
    print("Dataframe columns", df.columns)
    df = input_preprocessor.preprocess_input_data(df)

    results_total = total_trip_model.predict(df)
    results_duration = total_trip_model.predict(df)

    return (
        jsonify(
            {
                "fareAmount": f"${results_total[0]}",
                "duration": f"{results_duration[0]} min",
            }
        ),
        200,
    )
