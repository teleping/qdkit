# -*- coding: utf-8 -*-
"""
@Date ： 2026/3/17
@Auth ： zhangping
@Desc ：国泰君安API封装
"""
import pandas as pd, datetime as dt, requests, json, re

from .commons import config, logger

# pd.set_option("display.max_columns", None), pd.set_option("display.max_rows", None)
# pd.set_option("display.max_colwidth", None), pd.set_option("mode.use_inf_as_na", True)
# pd.set_option("display.width", None), pd.set_option("display.expand_frame_repr", False)

api_url = 'https://vip.gtjaqh.com:443/api/'

api_futures_contract = api_url + 'unicorn.cloudApi.contractTradeParams.query.do'  # 合约参数查询
api_futures_prices = api_url + 'unicorn.cloudApi.futuresContractPrice.queryByCode.do'  # 期货合约价格查询
api_futures_basis = api_url + 'unicorn.cloudApi.basisData.query.do'  # 基差数据查询
api_futures_inventory = api_url + 'unicorn.cloudApi.inventoryData.queryByCode.do'  # 库存数据查询
api_futures_profit = api_url + 'unicorn.cloudApi.processProfitData.queryByCode.do'  # 加工利润数据查询

# ==================== 请求头 ====================
request_header = {
    'accessKeyId': config['gtja']['access_key_id'],
    'accessKeySecret': config['gtja']['access_key_secret'],
    'Content-Type': 'application/json;charset=utf-8',
}

# ==================== 交易所编码映射 ====================
# 国君交易所编码 <-> 万得交易所编码 映射
gj_exchanges = ['CFFEX', 'CZCE', 'DCE', 'INE', 'SHFE', 'GFEX']
wd_exchanges = ['CFE', 'CZC', 'DCE', 'INE', 'SHF', 'GFE']
gj_to_wd = dict(zip(gj_exchanges, wd_exchanges))
wd_to_gj = dict(zip(wd_exchanges, gj_exchanges))


def _camel_to_snake(name):
    """驼峰命名转下划线命名"""
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def _get_date_str(date, format='%Y%m%d'):
    """获取日期字符串，参数为None时默认当天，支持date/datetime，支持整型/字符串如：'20260308'或'2026/03/08'或'2026-03-08'"""
    if date is None: date = dt.datetime.today()
    if isinstance(date, int): date = str(date)
    if isinstance(date, str): date = dt.datetime.strptime(date.replace('/', '').replace('-', ''), '%Y%m%d')
    if isinstance(date, dt.date): date = date.strftime(format)
    return date


def _api_query(api_url, params):
    """通用 POST 请求封装，返回 DataFrame，失败返回 None"""
    result = requests.request('POST', api_url, headers=request_header, data=json.dumps(params)).json()
    if result['code'] != 0:
        logger.error(f"{api_url} | {params} | {result['msg']}")
        return None
    df = pd.DataFrame(result['data'])
    # return df.rename(columns={col: camel_to_snake(col) for col in df.columns})
    return df


# ==================== 数据查询接口 ====================

def get_futures_contracts(date=None):
    """查询指定日期所有交易所的期货合约参数，返回合并后的 DataFrame"""
    results = []
    for e in gj_exchanges:
        result = _api_query(api_futures_contract, {'tradingDay': _get_date_str(date), 'exchangeCode': e})
        if result is not None: results.append(result)
    return pd.concat(results, ignore_index=True) if results else pd.DataFrame()


def get_futures_prices(date=None):
    """查询指定日期期货合约价格"""
    return _api_query(api_futures_prices, {'tradingDay': _get_date_str(date), 'exchangeCode': None})


def get_futures_basis(code=None, start_date=None, end_date=None):
    """查询期货基差数据，code 为合约代码，不传则查全部"""
    return _api_query(api_futures_basis, {
        'code': code,
        'startReportDate': _get_date_str(start_date, '%Y-%m-%d'),
        'endReportDate': _get_date_str(end_date, '%Y-%m-%d')
    })


def get_futures_inventory(code, report_date=None, start_date=None, end_date=None):
    """查询期货库存数据，code 为品种代码"""
    return _api_query(api_futures_inventory, {
        'code': code,
        # 'reportDate': _get_date_str(report_date, '%Y-%m-%d'),
        'startDataDate': _get_date_str(start_date, '%Y-%m-%d'),
        'endDataDate': _get_date_str(end_date, '%Y-%m-%d')
    })


def get_futures_profit(code, report_date=None, start_date=None, end_date=None):
    """查询期货加工利润数据，code 为品种代码"""
    return _api_query(api_futures_profit, {
        'code': code,
        # 'reportDate': _get_date_str(report_date, '%Y-%m-%d'),
        'startDataDate': _get_date_str(start_date, '%Y-%m-%d'),
        'endDataDate': _get_date_str(end_date, '%Y-%m-%d')
    })
