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

router = Blueprint("app_router", __name__)


@router.route("/predict", methods=["POST"])
def predict():
    """
    POST: Used in our frontend so we can upload and show an image.
    When it receives an image from the UI, it also calls our ML model to
    get and display the predictions.
    """

    print("request", request)

    return jsonify(
        {
            "fareAmount": "$12.00",
            "duration": "30 min",
        }
    )
