from flask import Flask, jsonify, request
import pandas as pd
from sqlalchemy import create_engine

app = Flask(_name_)

# Excel data reading
def read_excel_data():
    df = pd.read_excel('supermarkt_sales.xlsx')
    return df

# SQL data reading
def read_sql_data():
    engine = create_engine('sqlite:///sales.db')
    df = pd.read_sql('SELECT * FROM sales', con=engine)
    return df

# Endpoint for Excel data
@app.route('/api/xlsx', methods=['GET'])
def get_excel_data():
    df = read_excel_data()
    df = df.astype(str)  # convert all columns to string
    return jsonify(df.to_dict(orient='records'))

# Endpoint for SQL data
@app.route('/api/sql', methods=['GET'])
def get_sql_data():
    df = read_sql_data()
    df = df.astype(str)
    return jsonify(df.to_dict(orient='records'))

# Endpoint for sales data filtering
@app.route('/api/sales', methods=['GET'])
def get_sales_data():
    source = request.args.get('source', 'excel')  # default = excel
    if source == 'xlsx':
        df = read_excel_data()
    else:
        df = read_sql_data()
    df = df.astype(str)
    return jsonify(df.to_dict(orient='records'))

if _name_ == '_main_':
    app.run(debug=True)
