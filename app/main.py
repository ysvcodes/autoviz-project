"""
Author: autoviz-project user
File Purpose: Main application file for the autoviz-project.
              A simple Flask web server.
Dependencies: Flask
"""
import os
import pandas as pd
from flask import Flask, send_from_directory, jsonify, request, send_file

app_instance = Flask(__name__) # Renamed to avoid clash with 'app' in Dockerfile CMD if we use Gunicorn later
DATA_CSV = 'dashboard_data.csv'

@app_instance.route('/')
def dashboard():
    return send_from_directory('.', 'dashboard.html')

@app_instance.route('/api/dashboard-data')
def dashboard_data():
    if not os.path.exists(DATA_CSV) or os.stat(DATA_CSV).st_size == 0:
        return jsonify({"no_data": True})
    df = pd.read_csv(DATA_CSV)
    if df.empty:
        return jsonify({"no_data": True})
    data = {
        "subscribers": int(df['Subscribers'].sum()),
        "emailsSent": int(df['Emails Sent'].sum()),
        "engagement": {
            "labels": df['Month'].tolist(),
            "openRate": df['Open Rate'].tolist(),
            "clickRate": df['Click Rate'].tolist()
        },
        "campaigns": df.to_dict(orient='records')
    }
    return jsonify(data)

@app_instance.route('/api/import-csv', methods=['POST'])
def import_csv():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    file.save(DATA_CSV)
    return jsonify({"success": True})

@app_instance.route('/api/export-csv')
def export_csv():
    if not os.path.exists(DATA_CSV):
        return jsonify({"error": "No data to export"}), 404
    return send_file(DATA_CSV, as_attachment=True)

if __name__ == '__main__':
    app_instance.run(host='0.0.0.0', port=5000) 