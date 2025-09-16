# app.py (Flask Backend)
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os
import datetime

app = Flask(__name__)
CORS(app)

EXCEL_FILE = "supermarkt_sales.xlsx"

# Ensure Excel file exists with correct columns
if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=["timestamp", "category", "value"])
    df.to_excel(EXCEL_FILE, index=False)

@app.route("/data", methods=["POST"])
def add_data():
    """Receive JSON from frontend and store it in Excel"""
    payload = request.get_json()
    if not payload:
        return jsonify({"error": "No JSON received"}), 400

    try:
        category = payload["category"]
        value = float(payload["value"])
    except KeyError:
        return jsonify({"error": "Missing fields"}), 400

    timestamp = payload.get("timestamp", datetime.datetime.utcnow().isoformat())

    df = pd.read_excel(EXCEL_FILE)
    new_row = pd.DataFrame([{"timestamp": timestamp, "category": category, "value": value}])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_excel(EXCEL_FILE, index=False)

    return jsonify({"message": "Data saved", "record": new_row.to_dict(orient="records")[0]}), 201


@app.route("/data", methods=["GET"])
def get_data():
    """Send Excel data as JSON"""
    df = pd.read_excel(EXCEL_FILE)
    return jsonify(df.to_dict(orient="records")), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
