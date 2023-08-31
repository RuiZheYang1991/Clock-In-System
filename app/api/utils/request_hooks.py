import time
from flask import json
start_time = None

def before_request():
    global start_time
    start_time = time.time()

def after_request(response):
    if start_time:
        # 計算運算時間
        elapsed_time = time.time() - start_time
        # 添加到 JSON 中
        json_data = response.get_json()
        if json_data is None:
            json_data = {}
        json_data['Operation_time'] = str(round(elapsed_time,3))+' 秒'
        # 更新 Response
        response.set_data(json.dumps(json_data))
    return response

