from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import pandas as pd

from src.utils import predict

app = Flask(__name__)


cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


@app.route("/classify", methods=["POST"])
@cross_origin()
def classify():
    request_data = request.get_json()
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

@app.route("/test-classifier", methods=["GET"])
@cross_origin()
def test_classifier():
    df = pd.read_csv("Combined.csv").head(5)
    results = []
    for text in df["content"]:
        result = predict({"text": text})
        results.append(result)
    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
