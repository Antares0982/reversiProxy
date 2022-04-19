

#!/usr/bin/python3
import os
from configparser import ConfigParser

import requests
from flask import Flask, Response, request

cfgparser = ConfigParser()
cfgparser.read("config.ini")

app = Flask(__name__)


@app.after_request
def after_request(resp):
    """跨域支持."""
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Method'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return resp


@app.route('/ai_list', methods=['GET'])
def get_ai_map():
    ans = requests.get(
        f"http://{cfgparser['config']['ip']}:7685/ai_list").content
    return Response(ans, mimetype='application/json')


@app.route('/ai_api', methods=['POST'])
def ai_api():
    ans = requests.post(f"http://{cfgparser['config']['ip']}:7685/ai_api",
                        json=request.json).content
    return Response(ans, mimetype='application/json')


currentDir = os.path.dirname(os.path.abspath(__file__))
for file in os.listdir(currentDir):
    if file.endswith("pem"):
        PEM = os.path.join(currentDir, file)
    elif file.endswith("key"):
        KEY = os.path.join(currentDir, file)

# 挂载
if __name__ == '__main__':
    app.run(debug=False, port=7685, host='0.0.0.0', ssl_context=(PEM, KEY))
