# -*- coding: utf-8 -*-
"""
@Date ： 2026/3/28
@Auth ： zhangping
"""
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.types import VARCHAR, Date, DateTime, Integer, DECIMAL
from pangres import upsert
from .commons import config


class DBUtils:
    _engines = {}

    @classmethod
    def new_engine(cls, name, echo=False) -> Engine:
        conn_str = config['database'][name]
        connect_args = {'autocommit': True} if 'mssql' in conn_str else {}
        return create_engine(conn_str, pool_pre_ping=True, pool_size=10, max_overflow=10,
                             pool_recycle=3600, connect_args=connect_args, echo=echo)

    @classmethod
    def get_engine(cls, name) -> Engine:
        if name not in cls._engines.keys():
            cls._engines[name] = cls.new_engine(name, echo=False)
        return cls._engines[name]

    @classmethod
    def set_engine(cls, name, engine) -> Engine:
        existing = cls._engines.get(name)
        if existing is not None:
            existing.dispose()
        cls._engines[name] = engine
        return cls._engines[name]

    @classmethod
    def clear_engine(cls):
        for key in cls._engines:
            if cls._engines.get(key) is not None:
                cls._engines.get(key).dispose()
        cls._engines.clear()

    @classmethod
    def execute(cls, engine, sql):
        with Session(engine) as session:
            session.execute(text(sql) if isinstance(sql, str) else sql)
            session.commit()

    @classmethod
    def append(cls, conn, instances):
        if not isinstance(instances, list):
            instances = [instances]
        with Session(conn) as session:
            session.add_all(instances)
            session.commit()

    @classmethod
    def delete(cls, conn, instances):
        if not isinstance(instances, list):
            instances = [instances]
        with Session(conn) as session:
            for instance in instances:
                session.delete(instance)
            session.commit()

    @classmethod
    def truncate(cls, conn, table):
        cls.execute(conn, f'truncate {table}')

    @staticmethod
    def _df_types(df: pd.DataFrame):
        type_dict = {}
        for i, j in zip(df.columns, df.dtypes):
            if 'object' in str(j): type_dict.update({i: VARCHAR(length=255)})
            if 'float' in str(j): type_dict.update({i: DECIMAL(20, 5)})
            if 'int' in str(j): type_dict.update({i: Integer()})
            if 'datetime' in str(j): type_dict.update({i: DateTime()})
            elif 'date' in str(j): type_dict.update({i: Date()})
        return type_dict


class TableUpdater:
    def __init__(self, table_name: str, db: str = 'db_name', date_column: str = 'date',
                 code_column: str = 'code', engine: Engine = None):
        self.db = db
        self.engine = engine
        self.table = table_name.lower()
        self.date_column = None if date_column is None else date_column.lower()
        self.code_column = None if code_column is None else code_column.lower()

    def get_db(self):
        return self.db

    def get_table(self):
        return self.table

    def get_conn(self):
        self.engine = self.engine if self.engine is not None else DBUtils.new_engine(self.db)
        # print(self.engine.engine.pool.status())
        return self.engine

    def _get_code_condition(self, code):
        return f"and {self.code_column}='{code}'"

    def get_last_date(self, conditions='1=1'):
        if self.date_column is None: return None
        sql = f'select max({self.date_column}) date_max from {self.table} where {conditions}'
        df = pd.read_sql(sql, self.get_conn())
        last_date = df['date_max'][0] if df['date_max'][0] is not None else None
        return last_date

    def get_last_date_by_code(self, code, conditions='1=1'):
        if self.date_column is None: return None
        return self.get_last_date(conditions + ' ' + self._get_code_condition(code))

    def dispose(self):
        if self.engine is not None:
            self.engine.dispose()

    def delete_last_date(self):
        sql = f'delete from {self.table} where {self.date_column}=(select max({self.date_column}) from {self.table})'
        DBUtils.execute(self.get_conn(), sql)
        return self

    def delete_last_date_by_code(self, code):
        sql = f"delete from {self.table} where {self.date_column}=(select max({self.date_column}) from {self.table} where {self.code_column}='{code}') and {self.code_column}='{code}'"
        DBUtils.execute(self.get_conn(), sql)
        return self

    def truncate(self):
        DBUtils.truncate(self.get_conn(), self.table)
        return self

    def delete_by_code(self, code, conditions='1=1'):
        sql = f'delete from {self.table} where {conditions} {self._get_code_condition(code)}'
        DBUtils.execute(self.get_conn(), sql)
        return self

    def append(self, df):
        if df is not None and len(df) > 0:
            df.to_sql(name=self.table, con=self.get_conn(), dtype=DBUtils._df_types(df), if_exists='append',
                      index=False)
        return self

    def upsert(self, df: pd.DataFrame):
        if df is None or len(df) == 0: return 0
        return upsert(con=self.get_conn(), df=df, table_name=self.table, if_row_exists='update',
                      dtype=DBUtils._df_types(df), chunksize=1000, create_table=False)
