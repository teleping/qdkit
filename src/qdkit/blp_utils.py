#  -*- coding: utf-8 -*-
# @author: zhangping

import datetime as dt
from xbbg import blp


class BlpUtil:
    """
    彭博接口工具类
    """

    @classmethod
    def bdh(cls, ticker, flds='PX_LAST', start_date='20200101', end_date=None, overrides=None):
        """
        获取多时间序列数据
        ~~~~~~~~~~~~~~~~
        d = BlpUtil.bdh('600570 CH Equity', flds='PX_LAST', start_date='2021-04-01')
        """
        params = {'tickers': ticker, 'flds': flds, 'start_date': start_date, 'end_date': cls.get_date_str(end_date)}
        params = params if overrides is None else dict(list(params.items()) + list(overrides.items()))
        df = blp.bdh(**params)
        if df is not None and len(df) > 0:
            df = df[ticker]
            df = df.rename_axis('date').reset_index()
        return df

    @classmethod
    def get_date_str(cls, date, format='%Y%m%d'):
        date = date if date is not None else dt.datetime.today()
        date = date if type(date) == str else date.strftime(format)
        return date
