# -*- coding: utf-8 -*-
"""
@Date ： 2026/4/7
@Auth ： zhangping
@Desc ：东证期货 Finoview API封装
"""
import time, pandas as pd, datetime as dt, requests, json, re

from commons import config, logger

requests.packages.urllib3.disable_warnings()

_api_url = 'https://www.finoview.com.cn/autoApi/'

_api_index_catalogue = _api_url + 'CMS_CATALOGUE'  # 繁微指标目录
_api_index_data = _api_url + 'IndexData'  # 繁微指标数据
_api_spread_catalogue = _api_url + 'foreign/spread/spread_catalogue'  # 价差目录
_api_spread_ts_data = _api_url + 'foreign/spread/spread_ts_data'  # 价差时序

# ==================== 请求头 ====================
_params = {
    'appkey': config['dzqh']['app_key'],
    'appsecret': config['dzqh']['app_secret'],
}


def _get_date_str(date, format='%Y%m%d'):
    """获取日期字符串，参数为None时默认当天，支持date/datetime，支持整型/字符串如：'20260308'或'2026/03/08'或'2026-03-08'"""
    if date is None: date = dt.datetime.today()
    if isinstance(date, int): date = str(date)
    if isinstance(date, str): date = dt.datetime.strptime(date.replace('/', '').replace('-', ''), '%Y%m%d')
    if isinstance(date, dt.date): date = date.strftime(format)
    return date


def _api_query(api_url, params):
    """通用 POST 请求封装，返回 DataFrame，失败返回 None"""
    response = requests.request("POST", api_url, params={**_params, **params}, verify=False)
    result = json.loads(response.text)
    if result['code'] != '1':
        logger.error(f"{api_url} | {params} | {result['msg']}")
        return None
    return pd.DataFrame(result['data'])


def _api_query2(api_url, params):
    """通用 POST 请求封装，返回 DataFrame，失败返回 None"""
    response = requests.request("POST", api_url, json={**_params, **params}, verify=False)
    result = json.loads(response.text)
    if str(result['code']) != '1':
        logger.error(f"{api_url} | {params} | {result['message']}")
        return None
    return pd.DataFrame(result['data']['data'])


# ==================== 数据查询接口 ====================

def get_index_list(pages=300):
    """指标目录"""
    dfs = []
    for i in range(0, pages):
        dfs.append(_api_query(_api_index_catalogue, {'numpage': i}))
        time.sleep(1)
    return pd.concat(dfs, axis=0).reset_index(drop=True)


def get_index_data(id, start_date, end_date):
    """指标数据"""
    return _api_query(_api_index_data, {
        'superIndexLabel': id,
        'StartDate': _get_date_str(start_date),
        'EndDate': _get_date_str(end_date)
    })


def get_spread_list(type='基差'):
    """基差目录"""
    return _api_query2(_api_spread_catalogue, {'spread_type': type})


def get_spread_data(ids, start_date):
    """基差数据"""
    params = {
        'startdate': _get_date_str(start_date, format='%Y-%m-%d'),
        'spread_catalog_id': [ids] if isinstance(ids, str) else ids
    }
    response = requests.request("POST", _api_spread_ts_data, json={**_params, **params}, verify=False)
    result = json.loads(response.text)
    if str(result['code']) != '1':
        logger.error(f"{_api_spread_ts_data} | {params} | {result['message']}")
        return None

    dfs = []
    for r in result['data']['data']:
        df = pd.DataFrame(r['timeseries'])
        df['id'], df['name'] = r['id'], r['name']
        dfs.append(df)
    return pd.concat(dfs, axis=0).reset_index(drop=True)
