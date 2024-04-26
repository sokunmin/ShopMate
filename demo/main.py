import os
import requests
from flask import Flask, request, Response, jsonify, redirect
import time
import re

app = Flask(__name__, static_folder='static')

API_KEY = os.environ.get("GEMINI_API_KEY")
API_URL = "https://generativelanguage.googleapis.com"


@app.route('/source.html', methods=['GET'])
def source():
    git_url = "https://github.com/sokunmin/ShopMate"

    line = open("static/source.html")
    return line, 200

# user_usage = {}
@app.route('/', methods=['GET'])
def index():
    output = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="refresh" content="0;url=/gemini/static/index.html">
        <title>GenAI 2024, Shopmate, Loading</title>
    </head>
    <body>
        <p>Loading</p>
    </body>
    </html>"""
    return output, 200


@app.route('/<path:subpath>', methods=['POST'])
def handle_post_requests(subpath=''):
    try:
        # 获取 POST 请求的 JSON 数据
        json_data = request.get_json()
        if json_data is None:
            return jsonify({'error': 'No JSON data received'}), 400

        # 构造目标 URL
        target_url = f'https://generativelanguage.googleapis.com/{subpath}?key={API_KEY}'
        print("url=", target_url)

        # 发送 POST 请求到目标 URL，并将原始 JSON 数据作为请求体
        response = requests.post(target_url, json=json_data)

        # 返回目标 URL 的响应
        return response.content, response.status_code

    except Exception as e:
        return jsonify({'error': str(e)}), 500


from sys import platform

if platform == "darwin":
    if __name__ == '__main__':
        app.run(debug=True)
else:
    def main(request):
        def start_response(status, headers):
            response = Response(status=status)
            for header_name, header_value in headers:
                response.headers[header_name] = header_value
            return response

        return app.__call__(request.environ, start_response)
