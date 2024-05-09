import settings
from flask import Flask
from api import router
from flask_cors import CORS

app = Flask(__name__)
CORS(
    app,
    origins=["http://localhost:8080"],
    methods=["GET", "HEAD", "POST", "OPTIONS", "PUT", "PATCH", "DELETE"],
    resources=r"/*",
    allow_headers="*",
)

app.secret_key = "secret key"
app.register_blueprint(router)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=settings.API_DEBUG)
