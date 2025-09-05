#!/usr/bin/env python3
"""
Simple monitoring API for Quenito
"""

from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

@app.route('/status')
def status():
    """Simple status endpoint"""
    try:
        with open('/app/logs/status.json', 'r') as f:
            status_data = json.load(f)
    except:
        status_data = {
            "status": "waiting",
            "questions_completed": 0
        }
    
    return jsonify({
        "status": "running",
        "vnc_url": "vnc://localhost:5900",
        "model": "claude-sonnet-4-20250514",
        **status_data
    })

@app.route('/health')
def health():
    """Health check"""
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
