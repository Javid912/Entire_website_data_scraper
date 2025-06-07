import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, render_template, jsonify, request, send_file, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from config import Config
import subprocess
from datetime import datetime
import json

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

SCRAPED_JSON = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/scraped_data/kijufi_data.json'))
SCRAPED_CSV = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/scraped_data/kijufi_data.csv'))

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/results')
def results():
    return render_template('results.html')

@app.route('/api/scrape', methods=['POST'])
def api_scrape():
    url = request.form.get('url', 'https://kijufi.de/')
    scope = request.form.get('scope', 'site')
    out_format = request.form.get('format', 'json')
    scrapy_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../scrapy_project'))
    cmd = ['scrapy', 'crawl', 'kijufi_spider']
    start_time = datetime.now()
    try:
        subprocess.run(cmd, cwd=scrapy_dir, check=True)
        status = 'Scraping completed.'
    except Exception as e:
        status = f'Error: {e}'
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    preview = []
    try:
        with open(SCRAPED_JSON, 'r') as f:
            data = json.load(f)
            preview = data[:3] if isinstance(data, list) else []
    except Exception:
        preview = []
    return render_template('dashboard.html', status=status, url=url, scope=scope, out_format=out_format, duration=duration, preview=preview)

@app.route('/download/<format>')
def download_data(format):
    if format == 'json':
        if not os.path.exists(SCRAPED_JSON):
            return 'JSON result not found. Please run a scrape first.', 404
        return send_file(SCRAPED_JSON, as_attachment=True)
    elif format == 'csv':
        import pandas as pd
        if not os.path.exists(SCRAPED_JSON):
            return 'CSV result not found. Please run a scrape first.', 404
        if not os.path.exists(SCRAPED_CSV):
            try:
                df = pd.read_json(SCRAPED_JSON)
                df.to_csv(SCRAPED_CSV, index=False)
            except Exception as e:
                return f'Error converting to CSV: {e}', 500
        return send_file(SCRAPED_CSV, as_attachment=True)
    else:
        return 'Format not supported', 400

@app.route('/api/status')
def api_status():
    return jsonify({'status': 'idle'})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True) 