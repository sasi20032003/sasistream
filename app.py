from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
from sqlalchemy import create_engine
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access (e.g., Streamlit)

EXCEL_FILE = "supermarkt_sales.xlsx"
DB_FILE = "sales.db"

# Excel data reading
def read_excel_data():
    if not os.path.exists(EXCEL_FILE):
        return pd.DataFrame()  # Return empty DataFrame if file not found
    df = pd.read_excel(EXCEL_FILE)
    return df

# SQL data reading
def read_sql_data():
    if not os.path.exists(DB_FILE):
        return pd.DataFrame()
    engine = create_engine(f"sqlite:///{DB_FILE}")
    df = pd.read_sql("SELECT * FROM sales", con=engine)
    return df

# Endpoint for Excel data
@app.route("/api/xlsx", methods=["GET"])
def get_excel_data():
    df = read_excel_data()
    if df.empty:
        return jsonify({"error": "Excel file not found or empty"}), 404
    df = df.astype(str)  # convert all columns to string
    return jsonify(df.to_dict(orient="records"))

# Endpoint for SQL data
@app.route("/api/sql", methods=["GET"])
def get_sql_data():
    df = read_sql_data()
    if df.empty:
        return jsonify({"error": "Database not found or empty"}), 404
    df = df.astype(str)
    return jsonify(df.to_dict(orient="records"))

# Endpoint for sales data filtering (source=xlsx or source=sql)
@app.route("/api/sales", methods=["GET"])
def get_sales_data():
    source = request.args.get("source", "xlsx")  # default = xlsx
    if source == "xlsx":
        df = read_excel_data()
    else:
        df = read_sql_data()

    if df.empty:
        return jsonify({"error": f"No data found for source '{source}'"}), 404

    df = df.astype(str)
    return jsonify(df.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
