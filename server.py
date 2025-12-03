"""
Simple proxy server that serves frontend and proxies API requests to backend.
Run this single server and access everything on http://127.0.0.1:8080
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os

app = Flask(__name__, static_folder='frontend')
CORS(app)

BACKEND_URL = "http://127.0.0.1:8000"

# Serve frontend static files
@app.route('/')
def index():
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('frontend', filename)

# Proxy API requests to backend
@app.route('/api/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy_api(path):
    url = f"{BACKEND_URL}/api/{path}"
    
    # Forward the request to backend
    resp = requests.request(
        method=request.method,
        url=url,
        headers={key: value for key, value in request.headers if key != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False
    )
    
    # Return the response from backend
    return (resp.content, resp.status_code, resp.headers.items())

if __name__ == '__main__':
    print("=" * 50)
    print("WellnessAI Proxy Server")
    print("=" * 50)
    print(f"Frontend + API: http://127.0.0.1:8080")
    print(f"Backend API:    {BACKEND_URL}")
    print("=" * 50)
    app.run(debug=True, port=8080)
