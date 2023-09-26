from functools import wraps
from flask import jsonify

# 定义一个过滤空值响应参数的装饰器
def filter_null_values(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        response = f(*args, **kwargs)
        if response.mimetype == 'application/json':
            data = response.get_json()
            if data is not None:
                filtered_data = filter_null_values_in_dict(data)
                response.set_data(jsonify(filtered_data).get_data())

        return response

    return wrapper

def filter_null_values_in_dict(data):
    if isinstance(data, dict):
        return {k: filter_null_values_in_dict(v) for k, v in data.items() if v is not None}
    elif isinstance(data, (list, tuple)):
        return [filter_null_values_in_dict(item) for item in data if item is not None]
    else:
        return data