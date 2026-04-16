# qdkit

Quant Data Toolkits for python.

---

## 目录

- [安装](#install)
- [配置说明](#config)
- [国泰君安期货数据API (GTJA)](#gtja)
- [华泰证券数据API (HT_Insight)](#ht-insight)
- [东证期货 Finoview 数据API (DZQH)](#dzqh)

---



<a id="install"></a>
## 安装

```bash
pip install qdkit
```

---

<a id="config"></a>
## 配置说明

### 确保在项目中存在 `config.yaml` 和 `logs` 目录：

1. `config.yaml` 文件存在项目根目录下且配置完整；
2. `logs` 目录存在项目根目录下

---

### 配置文件位置

配置文件建议放在项目根目录 `config.yaml`，需要包含以下内容：

```yaml
app:
  name: myapp
  version: 0.1

logging:
  level: info

htzq:
  user: 'your_htzq_user'
  password: 'your_htzq_password'

gtja:
  access_key_id: 'your_access_key_id'
  access_key_secret: 'your_access_key_secret'

dzqh:
  app_key: 'your_app_key'
  app_secret: 'your_app_secret'
```

### 配置项说明


| 配置项                      | 说明                       |
| ------------------------ | ------------------------ |
| `htzq.user`              | 华泰证券用户名                  |
| `htzq.password`          | 华泰证券密码                   |
| `gtja.access_key_id`     | 国泰君安 API 访问密钥 ID         |
| `gtja.access_key_secret` | 国泰君安 API 访问密钥密码          |
| `dzqh.app_key`           | 东证期货 Finoview APP Key    |
| `dzqh.app_secret`        | 东证期货 Finoview APP Secret |


---



<a id="gtja"></a>
## 国泰君安期货数据API (GTJA)

国泰君安期货数据接口封装，提供期货合约、价格、基差、库存、加工利润等数据。

### 初始化

无需初始化，直接调用模块级函数。

首次使用前需要配置 API 访问密钥（`access_key_id` / `access_key_secret`）。

- 默认从项目根目录 `config.yaml` 的 `gtja` 节读取；
- 也可在运行时临时覆盖（适合测试或多账号切换）。

```python
from qdkit import gtja_api

# 方式：使用 config.yaml 中的 gtja 密钥（默认）
# gtja:
#   access_key_id: 'your_access_key_id'
#   access_key_secret: 'your_access_key_secret'
```

### 主要方法

#### 1. 查询期货合约参数

```python
# 查询指定日期所有交易所的期货合约参数
df = gtja_api.get_futures_contracts()

# 指定日期
df = gtja_api.get_futures_contracts(date='2026-03-31')

# 支持多种日期格式
df = gtja_api.get_futures_contracts(date=20260331)  # 整数
df = gtja_api.get_futures_contracts(date='2026/03/31')  # 斜杠分隔
df = gtja_api.get_futures_contracts(date=dt.datetime(2026, 3, 31))  # datetime 对象
```

#### 2. 查询期货合约价格

```python
# 查询指定日期期货合约价格
df = gtja_api.get_futures_prices()

# 指定日期
df = gtja_api.get_futures_prices(date='2026-03-31')
```

#### 3. 查询期货基差数据

```python
# 查询所有合约的基差数据
df = gtja_api.get_futures_basis()

# 查询指定合约的基差数据
df = gtja_api.get_futures_basis(
    'cu',         # code
    '2025-01-01', # start_date
    '2026-03-31'  # end_date
)
```

#### 4. 查询期货库存数据

```python
# 查询指定品种的库存数据
df = gtja_api.get_futures_inventory(
    'cu',         # code
    '2025-01-01', # start_date
    '2026-03-31'  # end_date
)
```

#### 5. 查询期货加工利润数据

```python
# 查询指定品种的加工利润数据
df = gtja_api.get_futures_profit(
    'cu',         # code
    '2025-01-01', # start_date
    '2026-03-31'  # end_date
)
```

### 交易所编码映射

国泰君安 API 支持以下交易所：


| 国泰君安编码 | 万得编码 | 说明         |
| ------ | ---- | ---------- |
| CFFEX  | CFE  | 中国金融期货交易所  |
| CZCE   | CZC  | 郑州商品交易所    |
| DCE    | DCE  | 大连商品交易所    |
| INE    | INE  | 上海国际能源交易中心 |
| SHFE   | SHF  | 上海期货交易所    |
| GFEX   | GFE  | 广州期货交易所    |


### 日期格式支持

所有日期参数支持以下格式：

```python
# 字符串格式
'2026-03-31'  # ISO 格式
'2026/03/31'  # 斜杠分隔
'20260331'    # 紧凑格式

# 整数格式
20260331

# datetime 对象
dt.datetime(2026, 3, 31)
dt.date(2026, 3, 31)

# None 表示当天
None  # 默认为当前日期
```

### 返回值

所有查询函数返回 `pandas.DataFrame`，查询失败返回 `None`。

```python
df = gtja_api.get_futures_contracts()
if df is not None:
    print(df.head())
    print(df.columns)
else:
    print("查询失败")
```

---



<a id="ht-insight"></a>
## 华泰证券数据API (HT_Insight)

华泰证券 Insight 数据接口封装，提供股票行情、财务数据、交易日历等功能。

### 初始化

```python
from qdkit.ht_insight import HT_Insight

# 方式1：使用配置文件中的用户名密码
ht = HT_Insight()

# 方式2：指定用户名密码
ht = HT_Insight(user='your_user', password='your_password')

# 方式3：上下文管理器（自动关闭连接）
with HT_Insight() as ht:
    data = ht.get_kline('600570.SH')
```

### 主要方法

#### 1. 获取所有股票信息

```python
# 获取所有上市交易的股票
df = ht.get_all_stocks_info()

# 指定日期范围和交易所
df = ht.get_all_stocks_info(
    start_date=dt.datetime(2020, 1, 1),
    end_date=dt.datetime(2026, 3, 31),
    exchange='XSHG',  # 上海交易所
    listing_state='上市交易'
)
```

#### 2. 获取K线数据

```python
# 获取单个股票日线数据
df = ht.get_kline('600570.SH')

# 指定时间范围和频率
df = ht.get_kline(
    codes='600570.SH',
    start_date=dt.datetime(2025, 1, 1),
    end_date=dt.datetime(2026, 3, 31),
    frequency='daily',  # 日线
    fq='none'  # 不复权
)

# 支持的频率：daily, weekly, monthly 等
```

#### 3. 获取日线基础数据

```python
# 获取股票日线基础数据（开高低收成交量等）
df = ht.get_daily_basic(
    code='600570.SH',
    start_date=dt.datetime(2025, 1, 1),
    end_date=dt.datetime(2026, 3, 31)
)
```

#### 4. 获取财务指标

```python
# 获取财务指标数据
df = ht.get_fin_indicator(
    code='600570.SH',
    start_date=dt.datetime(2020, 1, 1),
    end_date=dt.datetime(2026, 3, 31),
    period='Q4'  # Q1, Q2, Q3, Q4
)
```

#### 5. 获取股票估值数据

```python
# 获取股票估值数据（PE、PB等）
df = ht.get_stock_valuation(
    code='600570.SH',
    start_date=dt.datetime(2025, 1, 1),
    end_date=dt.datetime(2026, 3, 31)
)
```

#### 6. 获取财务报表

```python
# 获取利润表
df = ht.get_income_statement(
    code='600570.SH',
    start_date=dt.datetime(2020, 1, 1),
    end_date=dt.datetime(2026, 3, 31),
    period='Q4'
)

# 获取资产负债表
df = ht.get_balance_sheet(
    code='600570.SH',
    period='Q4'
)

# 获取现金流量表
df = ht.get_cashflow_statement(
    code='600570.SH',
    period='Q4'
)
```

#### 7. 获取可转债数据

```python
# 获取新发行可转债信息
df = ht.get_new_con_bond()
```

#### 8. 获取交易日历

```python
# 获取指定交易所的交易日
df = ht.get_trading_days(
    start_date=dt.datetime(2025, 1, 1),
    end_date=dt.datetime(2026, 3, 31),
    exchange='XSHG'  # XSHG(上海), XSHE(深圳)
)
```

#### 9. 获取行业分类

```python
# 获取行业分类信息
df = ht.get_industries(name='sw_l1')  # 申万一级行业

# 获取股票所属行业
df = ht.get_industry(
    code='600570.SH',
    classified='sw'  # sw(申万), jyj(经济景气)
)
```

#### 10. 获取指数成分

```python
# 获取指数成分股
df = ht.get_index_component(
    code='000300.SH',  # 沪深300
    date=dt.datetime(2026, 3, 31)
)
```

#### 11. 获取版本信息

```python
version = HT_Insight.get_version()
print(f"Insight API 版本: {version}")
```

#### 12. 连接管理

```python
# 重新登录
ht.re_login()

# 关闭连接
ht.close()
```

### 参数说明


| 参数                 | 类型   | 说明                  |
| ------------------ | ---- | ------------------- |
| `user`             | str  | 华泰证券用户名，不指定则从配置文件读取 |
| `password`         | str  | 华泰证券密码，不指定则从配置文件读取  |
| `login_log`        | bool | 是否打印登录日志，默认 False   |
| `open_trace`       | bool | 是否开启追踪，默认 False     |
| `open_file_log`    | bool | 是否写入文件日志，默认 False   |
| `open_console_log` | bool | 是否打印控制台日志，默认 False  |


---



## 东证期货 Finoview 数据API (DZQH)

东证期货 Finoview 数据接口封装，提供繁微指标目录、指标时序数据、期货市场价差目录和价差时序数据查询功能。

### 初始化

无需实例化，直接调用模块级函数。

```python
from qdkit import dzqh_api
import datetime as dt
```

首次使用前需要在 `config.yaml` 中配置接口密钥：

```yaml
dzqh:
  app_key: 'your_app_key'
  app_secret: 'your_app_secret'
```

### 主要方法

#### 1. 获取繁微指标目录

```python
# 获取指标目录
df = dzqh_api.get_index_list()

# 只抓取前 10 页，适合测试
df = dzqh_api.get_index_list(pages=10)
```

#### 2. 获取繁微指标数据

```python
# 查询单个指标在指定时间区间内的数据
df = dzqh_api.get_index_data(
    id='DZ00012732',
    start_date='2019-04-01',
    end_date='2019-04-19'
)

# 支持 datetime / date / int / str
df = dzqh_api.get_index_data(
    id='DZ00012732',
    start_date=dt.datetime(2026, 1, 1),
    end_date=dt.date(2026, 3, 31)
)
```

#### 3. 获取期货价差目录

```python
# 当前默认查询“基差”目录
df = dzqh_api.get_spread_list()

# 显式指定价差类型
df = dzqh_api.get_spread_list(type='基差')
```

#### 4. 获取期货价差时序数据

```python
# 查询单个价差 ID 的时序数据
df = dzqh_api.get_spread_data(
    ids='BASIS_001',
    start_date='2025-01-01'
)

# 一次查询多个价差 ID
df = dzqh_api.get_spread_data(
    ids=['BASIS_001', 'BASIS_002'],
    start_date=dt.datetime(2025, 1, 1)
)
```

---

## 使用示例

### 示例1：获取股票K线数据并保存

```python
from qdkit.ht_insight import HT_Insight
import datetime as dt

with HT_Insight() as ht:
    # 获取浦发银行近一年的日线数据
    df = ht.get_kline(
        codes='600000.SH',
        start_date=dt.datetime(2025, 3, 31),
        end_date=dt.datetime(2026, 3, 31)
    )
    
    # 保存为 CSV
    df.to_csv('600000_kline.csv', index=False)
    print(f"获取 {len(df)} 条数据")
```

### 示例2：获取期货基差数据

```python
from qdkit import gtja_api
import datetime as dt

# 获取沪铜期货近三个月的基差数据
df = gtja_api.get_futures_basis(
    'cu',
    dt.datetime(2025, 12, 31),
    dt.datetime(2026, 3, 31)
)

if df is not None:
    print(df.head(10))
```

### 示例3：获取多个股票的财务数据

```python
from qdkit.ht_insight import HT_Insight
import datetime as dt

codes = ['600000.SH', '600570.SH', '601988.SH']

with HT_Insight() as ht:
    for code in codes:
        df = ht.get_fin_indicator(
            code=code,
            start_date=dt.datetime(2020, 1, 1),
            end_date=dt.datetime(2026, 3, 31),
            period='Q4'
        )
        print(f"{code}: {len(df)} 条财务数据")
```

### 示例4：先查价差目录，再取价差时序

```python
from qdkit import dzqh_api

# 1. 获取“基差”目录
catalog = dzqh_api.get_spread_list(type='基差')

# 2. 取前两个目录 ID
ids = catalog['id'].head(2).tolist()

# 3. 获取价差时序数据
df = dzqh_api.get_spread_data(ids=ids, start_date='2025-01-01')

print(df.head())
```

---

