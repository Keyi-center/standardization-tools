from flask import jsonify
from base_util.filter_null_params import filter_null_values

@filter_null_values
def response(code, message, data=None):
    return jsonify({"code": code, "message": message, "data": data})


def ok(data, message="successful"):
    return response(200, message, data)


def ok_list(result_list, total=None, page_no=None, page_size=None):
    if total is None:
        total = len(result_list)
    return ok({"list": result_list, "total": total, "page_no": page_no, "page_size": page_size})


def not_found(message="not found"):
    return response(404, message)


def internal_error(message="internal_error"):
    return response(500, message)


def error(code, message):
    return response(code, message)
