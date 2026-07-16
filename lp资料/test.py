import hashlib
import json
import time
import uuid

import requests

BASE_URL = "https://test-data-open-platform.leapmotor.com"
APP_ID = "57fb1e5c037a4e2ca0d8e20a20114173"
APP_SECRET = "czjVYxu1RqcD4TdGYmDDP7rcqay0zTKxUfLrfE/YUayCv0nkeHwD79a4FD3zqmIG"


def convert_value_to_string(value):
    """将参数值转换为签名字符串"""
    if value is None:
        return ""
    if isinstance(value, dict):
        return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    if isinstance(value, (list, tuple)):
        return ",".join(str(x) for x in value)
    return str(value)


def generate_signature(timestamp, nonce, path_vars=None, query_params=None):
    """
    生成SHA-256 + HEX签名
    算法：收集所有参数(header的timestamp/nonce + path变量 + query参数 + appSecret)，
    值扁平化为字符串，按key字典序排序，拼接为 key1=value1#key2=value2#...，
    SHA256哈希后HEX编码
    """
    params = {}
    params["timestamp"] = str(timestamp)
    params["nonce"] = nonce
    params["appSecret"] = APP_SECRET

    if path_vars:
        for k, v in path_vars.items():
            params[k] = convert_value_to_string(v)

    if query_params:
        for k, v in query_params.items():
            params[k] = convert_value_to_string(v)

    sorted_keys = sorted(params.keys())
    content = "#".join(f"{k}={params[k]}" for k in sorted_keys)
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def build_headers(path_vars=None, query_params=None):
    """构建请求头"""
    timestamp = int(time.time() * 1000)
    nonce = uuid.uuid4().hex
    signature = generate_signature(timestamp, nonce, path_vars, query_params)
    return {
        "X-App-Id": APP_ID,
        "X-Signature": signature,
        "X-Timestamp": str(timestamp),
        "X-Nonce": nonce,
    }


def get_mileage(vin, begin_time):
    """查询里程数据"""
    path = f"/api/v1/cars/{vin}/trace-points/mileage"
    query_params = {
        "beginTime": begin_time,
        # "endTime": end_time,
        # "pageNum": str(page_num),
        # "pageSize": str(page_size),
    }
    headers = build_headers(path_vars={"vin": vin}, query_params=query_params)
    resp = requests.get(BASE_URL + path, headers=headers, params=query_params)
    print(f"里程数据 (VIN={vin}):")
    print(json.dumps(resp.json(), indent=2, ensure_ascii=False))
    return resp.json()


def get_speed_energy(vin, begin_time):
    """查询速度能耗数据"""
    path = f"/api/v1/cars/{vin}/trace-points/speed-energy"
    query_params = {
        "beginTime": begin_time,
        # "endTime": end_time,
        # "pageNum": str(page_num),
        # "pageSize": str(page_size),
    }
    headers = build_headers(path_vars={"vin": vin}, query_params=query_params)
    resp = requests.get(BASE_URL + path, headers=headers, params=query_params)
    print(f"速度能耗数据 (VIN={vin}):")
    print(json.dumps(resp.json(), indent=2, ensure_ascii=False))
    return resp.json()


def get_acceleration_braking(vin, begin_time):
    """查询加减速数据"""
    path = f"/api/v1/cars/{vin}/trace-points/acceleration-braking"
    query_params = {
        "beginTime": begin_time,
        # "endTime": end_time,
        # "pageNum": str(page_num),
        # "pageSize": str(page_size),
    }
    headers = build_headers(path_vars={"vin": vin}, query_params=query_params)
    resp = requests.get(BASE_URL + path, headers=headers, params=query_params)
    print(f"加减速数据 (VIN={vin}):")
    print(json.dumps(resp.json(), indent=2, ensure_ascii=False))
    return resp.json()


def get_steering_wheel(vin, begin_time):
    """查询方向盘数据"""
    path = f"/api/v1/cars/{vin}/trace-points/steering-wheel"
    query_params = {
        "beginTime": begin_time,
        # "endTime": end_time,
        # "pageNum": str(page_num),
        # "pageSize": str(page_size),
    }
    headers = build_headers(path_vars={"vin": vin}, query_params=query_params)
    resp = requests.get(BASE_URL + path, headers=headers, params=query_params)
    print(f"方向盘数据 (VIN={vin}):")
    print(json.dumps(resp.json(), indent=2, ensure_ascii=False))
    return resp.json()


def get_trace_view(vin, trace_type, begin_time):
    """查询行车轨迹视图"""
    path = f"/api/v1/cars/{vin}/trace-points/view"
    query_params = {
        "type": str(trace_type),
        "beginTime": begin_time,
        "endTime": end_time,
        # "pageNum": str(page_num),
        # "pageSize": str(page_size),
    }
    headers = build_headers(path_vars={"vin": vin}, query_params=query_params)
    resp = requests.get(BASE_URL + path, headers=headers, params=query_params)
    print(f"行车轨迹视图 (VIN={vin}):")
    print(json.dumps(resp.json(), indent=2, ensure_ascii=False))
    return resp.json()


if __name__ == "__main__":
    VIN = "LFZ63AV56RD000089"
    BEGIN_TIME = "2026-07-09 00:00:00"
    END_TIME = "2026-07-10 23:59:59"

    get_mileage(VIN, BEGIN_TIME)
    print("-" * 60)
    get_speed_energy(VIN, BEGIN_TIME)
    print("-" * 60)
    get_acceleration_braking(VIN, BEGIN_TIME)
    print("-" * 60)
    get_steering_wheel(VIN, BEGIN_TIME)
    print("-" * 60)
    get_trace_view(VIN, "speed-energy", BEGIN_TIME)
