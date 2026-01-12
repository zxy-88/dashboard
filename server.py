from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import requests
import re
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    return send_file('data_fetch.html')

@app.route('/search_window.html')
def search_window():
    return send_file('search_window.html')

@app.route('/api/fetch-data')
def fetch_data():
    try:
        # Get date parameters
        start_date = request.args.get('start_date', '')
        end_date = request.args.get('end_date', '')
        
        if not start_date or not end_date:
            return jsonify({'error': 'Missing date parameters'}), 400
        
        # Parse dates (format: YYYY-MM-DD)
        start_parts = start_date.split('-')
        end_parts = end_date.split('-')
        
        sd = start_parts[2]  # day
        sm = start_parts[1]  # month
        sy = start_parts[0]  # year
        
        ed = end_parts[2]
        em = end_parts[1]
        ey = end_parts[0]
        
        # Build URL
        import time
        timestamp = int(time.time() * 1000)
        url = f"https://cloud.isurvey.mobi/web/php/report/get_data_report.php?_dc={timestamp}&con_date=2&date_from={sd}%2F{sm}%2F{sy}&date_to={ed}%2F{em}%2F{ey}&empcode=&closeby=&appv_status=&branch_id=&report_type=enquiry&inscompany=&page=1&start=0&limit=500"
        
        # Fetch data from external API
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Parse JSON from response
        content = response.text
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        
        if not json_match:
            return jsonify({'error': 'No JSON data found in response'}), 500
        
        data = json.loads(json_match.group())
        arr_data = data.get('arr_data', [])
        
        # Debug: Print field names
        if arr_data:
            print("📊 Sample data fields:", list(arr_data[0].keys()))
            print("📋 First row:", arr_data[0])
        
        return jsonify({
            'success': True,
            'data': arr_data,
            'count': len(arr_data)
        })
        
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Request failed: {str(e)}'}), 500
    except json.JSONDecodeError as e:
        return jsonify({'error': f'JSON parse error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Server running at http://127.0.0.1:5000")
    app.run(debug=True,host='0.0.0.0', port=5000)
