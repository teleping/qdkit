#  -*- coding: utf-8 -*-
# @author: zhangping

import datetime as dt, pandas as pd
from insight_python.com.insight import common
from insight_python.com.insight import query
from insight_python.com.insight.market_service import market_service


class HT_Insight():

    def __init__(self, user='******', password='******', login_log=False, open_trace=False,
                 open_file_log=False, open_console_log=False):
        self.user = user
        self.password = password
        self.login_log = login_log
        self.open_trace = open_trace
        self.open_file_log = open_file_log
        self.open_console_log = open_console_log
        self.re_login()

    def re_login(self):
        # print(self.get_version())
        common.login(InsightMarketService(), self.user, self.password, login_log=self.login_log)
        common.config(self.open_trace, self.open_file_log, self.open_console_log)

    @staticmethod
    def get_version(cls):
        return common.get_version()

    def close(self):
        common.fini()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
        return True

    def get_all_stocks_info(self, start_date: dt.datetime = None, end_date: dt.datetime = None, exchange=None,
                            listing_state='上市交易'):
        start_date = dt.datetime(1989, 1, 1) if start_date is None else start_date
        end_date = dt.datetime.now() if end_date is None else end_date
        return query.get_all_stocks_info(listing_date=[start_date, end_date], exchange=exchange,
                                         listing_state=listing_state)

    def get_kline(self, codes, start_date: dt.datetime = dt.datetime(2015, 1, 1),
                  end_date: dt.datetime = dt.datetime.now(),
                  frequency="daily", fq="none"):
        return query.get_kline(htsc_code=codes, time=[start_date, end_date], frequency=frequency, fq=fq)

    def get_fin_indicator(self, code, start_date: dt.datetime = None, end_date: dt.datetime = None, period='Q4'):
        start_date = dt.datetime(2015, 1, 1) if start_date is None else start_date
        end_date = dt.datetime.now() if end_date is None else end_date
        return query.get_fin_indicator(htsc_code=code, end_date=[start_date, end_date], period=period)

    def get_stock_valuation(self, code, start_date: dt.datetime = None, end_date: dt.datetime = None):
        start_date = dt.datetime(2015, 1, 1) if start_date is None else start_date
        end_date = dt.datetime.now() if end_date is None else end_date
        return query.get_stock_valuation(htsc_code=code, trading_day=[start_date, end_date])

    def get_income_statement(self, code, start_date: dt.datetime = None, end_date: dt.datetime = None, period='Q4'):
        start_date = dt.datetime(2015, 1, 1) if start_date is None else start_date
        end_date = dt.datetime.now() if end_date is None else end_date
        return query.get_income_statement(htsc_code=code, end_date=[start_date, end_date], period=period)

    def get_balance_sheet(self, code, start_date: dt.datetime = None, end_date: dt.datetime = None, period='Q4'):
        start_date = dt.datetime(2015, 1, 1) if start_date is None else start_date
        end_date = dt.datetime.now() if end_date is None else end_date
        return query.get_balance_sheet(htsc_code=code, end_date=[start_date, end_date], period=period)

    def get_cashflow_statement(self, code, start_date: dt.datetime = None, end_date: dt.datetime = None, period='Q4'):
        start_date = dt.datetime(2015, 1, 1) if start_date is None else start_date
        end_date = dt.datetime.now() if end_date is None else end_date
        return query.get_cashflow_statement(htsc_code=code, end_date=[start_date, end_date], period=period)

    def get_new_con_bond(self):
        return query.get_new_con_bond()

    def get_trading_days(self, start_date: dt.datetime = None, end_date: dt.datetime = None, exchange='XSHG'):
        start_date = dt.datetime(2015, 1, 1) if start_date is None else start_date
        end_date = dt.datetime.now() if end_date is None else end_date
        print(exchange, start_date, end_date)
        return pd.DataFrame(
            query.get_trading_days(exchange=exchange, trading_day=[start_date, end_date], count=None)[1])

    def get_industries(self, name='sw_l1'):
        return query.get_industries(classified=name)

    def get_index_component(self, code, date):
        return query.get_index_component(code, None, None, date)


class InsightMarketService(market_service):
    def on_query_response(self, result):
        for response in iter(result):
            print(response)
