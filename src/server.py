from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import logging

from src.utils import predict

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


@app.route("/classify", methods=["POST"])
@cross_origin()
def classify():
    request_data = request.get_json()
    logger.info(f"Request data keys: {list(request_data.keys()) if request_data else 'None'}")
    result = predict(request_data)
    return jsonify(result)


@app.route("/bulk-classify", methods=["POST"])
@cross_origin()
def bulk_classify():
    request_data = request.get_json()
    result = []
    for issue in request_data:
        result.append(predict(issue))
    return jsonify(result)


@app.route("/health", methods=["GET"])
@cross_origin()
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok", "message": "HCI Classifier API is running"})


@app.route("/", methods=["GET"])
@cross_origin()
def root():
    """Root endpoint - Returns API information"""
    return jsonify({
        "name": "HCI Classifier API",
        "version": "1.0",
        "endpoints": {
            "/classify": "POST - Classify text(s)",
            "/bulk-classify": "POST - Bulk classify multiple texts",
            "/health": "GET - Health check"
        }
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
