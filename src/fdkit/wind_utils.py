#  -*- coding: utf-8 -*-
# @author: zhangping

import logging
import pandas as pd
import datetime as dt
from WindPy import w


def startwind(fn):
    """
    wind接口初始化
    """

    def wrapper(*args1, **args2):
        if not w.isconnected():
            w.start()
        return fn(*args1, **args2)

    return wrapper


class WindUtil:
    """
    Wind接口工具类
    """

    @classmethod
    @startwind
    def tdays(cls, start_date, end_date=None):
        '''
        获取交易日
        ~~~~~~~~~~~~~~~~
        l = WindUtil.tdays('2020-03-07')
        l = WindUtil.tdays('2020-03-07', end_date='2020-04-07')
        '''
        l = w.tdays(cls.get_date_str(start_date), cls.get_date_str(end_date), "").Data
        return l[0] if l is not None and len(l) > 0 else []

    @classmethod
    @startwind
    def sectors(cls, sectorid, date=None):
        """
        获取板块成分(通过Wind板块ID)
        ~~~~~~~~~~~~~~~~
        df = WindUtil.sectors('a001010100000000') #当前全部A股
        df = WindUtil.sectors('1000010084000000', date='2020-08-28') #国内商品品种
        """
        wd = w.wset('sectorconstituent', f'sectorid={sectorid};date={cls.get_date_str(date)}', usedf=True)
        if wd[0] != 0: logging.error(f' wind error: {wd[0]}')
        return wd[1] if wd[0] == 0 else None

    @classmethod
    @startwind
    def sectors_by_code(cls, wind_code, date=None):
        """
        获取板块成分(通过Wind代码)
        ~~~~~~~~~~~~~~~~
        df = WindUtil.sectors_by_code('APFI.WI', date='2020-08-28') #Wind农产品指数
        df = WindUtil.sectors_by_code('000300.SH') #沪深300成分股
        """
        wd = w.wset('sectorconstituent', f'windcode={wind_code};date={cls.get_date_str(date)}', usedf=True)
        if wd[0] != 0: logging.error(f' wind error: {wd[0]}')
        return wd[1] if wd[0] == 0 else None

    @classmethod
    @startwind
    def fu_contracts(cls, wind_code, start_date=None, end_date=None):
        """
        获取品种期货合约
        ~~~~~~~~~~~~~~~~
        df = WindUtil.fu_contracts('A.DCE') #获取品种合约
        """
        wd = w.wset('futurecc',
                    f'wind_code={wind_code};startdate={cls.get_date_str(start_date)};enddate={cls.get_date_str(end_date)}',
                    usedf=True)
        if wd[0] != 0: logging.error(f' wind error: {wd[0]}')
        return wd[1] if wd[0] == 0 else None

    @classmethod
    @startwind
    def fu_hiscode(cls, wind_code, trade_date=None):
        """
        获取主力合约代码
        ~~~~~~~~~~~~~~~~
        code = WindUtil.fu_hiscode('A.DCE') #获取品种合约
        """
        wd = w.wss(wind_code, 'trade_hiscode', f'tradeDate={cls.get_date_str(trade_date, "%Y%m%d")}', usedf=True)
        if wd[0] != 0: logging.error(f' wind error: {wd[0]}')
        hiscode = wd[1]['TRADE_HISCODE'][0] if wd[0] == 0 else None
        return hiscode if wind_code != hiscode else None

    @classmethod
    @startwind
    def wsd(cls, codes, fields, start_date=None, end_date=None, options=None):
        """
        获取多品种单指标或单品种多指标的时间序列数据
        ~~~~~~~~~~~~~~~~
        df = WindUtil.wsd('600570.SH', 'open,close,high,low')
        df = WindUtil.wsd('600570.SH', 'open,close,high,low', start_date='2021-04-01', end_date='2021-04-05', options='')
        """
        df = None
        wd = w.wsd(codes, fields, cls.get_date_str(start_date), cls.get_date_str(end_date), options)
        if wd.ErrorCode != 0: logging.error(f' wind error: {wd.ErrorCode}')
        if wd is not None and wd.ErrorCode == 0 and len(wd.Times) > 0 and len(wd.Data[0]) > 0:
            data = {'date': wd.Times}
            for idx, field in enumerate(wd.Fields):
                data[field] = wd.Data[idx]
            df = pd.DataFrame(data)
        return df

    @classmethod
    @startwind
    def wset(cls, name, options):
        """
        用来获取数据集信息，包括板块成分、指数成分、ETF申赎成分信息等
        ~~~~~~~~~~~~~~~~
        df = WindUtil.wset('sectorconstituent', 'date=2022-02-18;windcode=801080.SI') # 获取 801080.SI的成分和权重
        """
        wd = w.wset(name, options, usedf=True)
        if wd[0] != 0: logging.error(f' wind error: {wd[0]}')
        return wd[1] if wd[0] == 0 else None

    # @classmethod
    # @startwind
    # def wss(cls, codes, field, options=None):
    #     """
    #     df = WindUtil.wss('1000015232000000', 'superiorcode', options)
    #     """
    #     df = None
    #     wd = w.wss(codes, field, options)
    #     if wd.ErrorCode != 0: logging.error(f' wind error: {wd.ErrorCode}')
    #     if wd is not None and wd.ErrorCode == 0 and len(wd.Data[0]) > 0:
    #         data = {}
    #         for idx, field in enumerate(wd.Fields):
    #             data[field] = wd.Data[idx]
    #         df = pd.DataFrame(data)
    #     return df

    @classmethod
    @startwind
    def wss(cls, codes, fields, options=None):
        """
        WSS多维数据
        ~~~~~~~~~~~~~~~~
        code = WindUtil.wss('110095.SH,127084.SZ', 'underlyingcode,underlyingname,clause_conversion2_swapshareprice', 'tradeDate=20240711;unit=1;date=20240711')
        """
        wd = w.wss(codes, fields, options=options, usedf=True)
        if wd[0] != 0: logging.error(f' wind error: {wd[0]}')
        return wd[1] if wd[0] == 0 else None

    @classmethod
    @startwind
    def edb(cls, codes, start_date=None, end_date=None, options=None):
        """
        获取多宏观经济数据
        ~~~~~~~~~~~~~~~~
        df = WindUtil.edb('S0049582')
        df = WindUtil.edb('S0049582', start_date='2020-01-01', end_date='2021-04-01', options='')
        """
        df = None
        wd = w.edb(codes, cls.get_date_str(start_date), cls.get_date_str(end_date), options)
        if wd.ErrorCode != 0: logging.error(f' wind error: {wd.ErrorCode}')
        if wd is not None and wd.ErrorCode == 0 and len(wd.Times) > 0 and len(wd.Data[0]) > 0:
            data = {'date': wd.Times}
            for idx, field in enumerate(wd.Fields):
                data[field] = wd.Data[idx]
            df = pd.DataFrame(data)
        return df

    @classmethod
    @startwind
    def wses(cls, codes, field, start_date=None, end_date=None, options=None):
        """
        获取多品种单指标或单品种多指标的时间序列数据
        ~~~~~~~~~~~~~~~~
        df = WindUtil.wses('1000015232000000', 'sec_close_avg', start_date='2021-04-01', end_date='2021-04-05', options='')
        """
        df = None
        wd = w.wses(codes, field, cls.get_date_str(start_date), cls.get_date_str(end_date), options)
        if wd.ErrorCode != 0: logging.error(f' wind error: {wd.ErrorCode}')
        if wd is not None and wd.ErrorCode == 0 and len(wd.Times) > 0 and len(wd.Data[0]) > 0:
            data = {'date': wd.Times}
            for idx, field in enumerate(wd.Fields):
                data[field] = wd.Data[idx]
            df = pd.DataFrame(data)
        return df

    @classmethod
    def get_date_str(cls, date, fmt='%Y-%m-%d'):
        date = date if date is not None else dt.datetime.today()
        return date if isinstance(date, str) else date.strftime(fmt)
