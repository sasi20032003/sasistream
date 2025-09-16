from flask import Flask, jsonify, request
import pandas as pd
from sqlalchemy import create_engine

# FIX: Use __name__ instead of _name_
app = Flask(__name__)

# Excel data reading
def read_excel_data():
    try:
        df = pd.read_excel('supermarkt_sales.xlsx')
        return df
    except Exception as e:
        return pd.DataFrame({"error": [str(e)]})

# SQL data reading
def read_sql_data():
    try:
        engine = create_engine('sqlite:///sales.db')
        df = pd.read_sql('SELECT * FROM sales', con=engine)
        return df
    except Exception as e:
        return pd.DataFrame({"error": [str(e)]})

# Endpoint for Excel data
@app.route('/api/xlsx', methods=['GET'])
def get_excel_data():
    df = read_excel_data()
    df = df.astype(str)  # Ensure everything is JSON serializable
    return jsonify(df.to_dict(orient='records'))

# Endpoint for SQL data
@app.route('/api/sql', methods=['GET'])
def get_sql_data():
    df = read_sql_data()
    df = df.astype(str)
    return jsonify(df.to_dict(orient='records'))

# Endpoint for sales data filtering (optional)
@app.route('/api/sales', methods=['GET'])
def get_sales_data():
    source = request.args.get('source', 'xlsx')  # Default to Excel
    if source == 'xlsx':
        df = read_excel_data()
    else:
        df = read_sql_data()
    df = df.astype(str)
    return jsonify(df.to_dict(orient='records'))

# FIX: Correct the main block
if __name__ == '__main__':
    app.run(debug=True, port=5000)
