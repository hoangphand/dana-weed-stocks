import json
# import sqlite3
import mysql.connector 
# from python_mysql_dbconfig import read_db_config

import sys
import glob
import errno
import datetime
import calendar
from datetime import datetime
############# Didn't work
# db_config = read_db_config()
# conn =MySQLConnection(**db_config)
########################
# MySQL commands to find host:
# select @@hostname;
#  show variables where Variable_name like '%host%';
mydb = mysql.connector.connect(
  # host="weeddb.cbdkoamqrvfd.us-west-2.rds.amazonaws.com",
  host="localhost",
  user="root",
  passwd="6617WoOD315!",
  database="symbol_prices",
  buffered=True
)
# mydb = mysql.connector.connect(
#   host="localhost",
#   user="danaaesch",
#   passwd="WoodHorse41!!",
#   database="symbol_prices"
# )
# # SELECT USER(),CURRENT_USER();
# print(mydb)
# # conn = sqlite3.connect('symbols_times_info.sqlite')
cur = mydb.cursor()
# cur.execute("CREATE DATABASE symbol_prices")
# cur.execute("SHOW DATABASES")
# 
# for x in cur:
#   print(x)
# 
# # Note that AlphaVantage has many APIs. We just decided on the 5-min one w/ open, high, low, close, and volume but we may want to reconsider this in the future.
# # Oct 15, 2018: Note that support@alphavantage.co seems to be switching the '3. Last Refreshed' field of their API currently.
# # Today, it seems that the time given is the start of their 5-min periods but this may change so might be to check this from time to time
# # Do some setup
# cur.executescript('''
SQL='''
DROP TABLE IF EXISTS Symbol;
DROP TABLE IF EXISTS Five_mins;
DROP TABLE IF EXISTS Symbol_five_mins;
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS Symbol_five_min;
CREATE TABLE Symbol (
    id     INT NOT NULL AUTO_INCREMENT,
    symbol  VARCHAR(50) UNIQUE,
    PRIMARY KEY(id));
CREATE TABLE Five_mins (
    id  INT NOT NULL AUTO_INCREMENT,
    five_min_start  INTEGER UNIQUE,
    PRIMARY KEY(id));
CREATE TABLE Symbol_five_mins (
    symbol_id     INT,
    five_min_start_id   INT,
    open        REAL,
    high    REAL,
    low REAL,
    close REAL,
    volume INT,
    PRIMARY KEY (symbol_id, five_min_start_id))
'''
# for result in cur.execute(SQL, multi=True):
#    pass
# mydb.commit()
print('here')
# Need to have something like :
# for result in cur.execute("SHOW TABLES"):
#    print(result)

# for x in cur:
#     print(x)
# Each json file contains a two-element dictionary. First entry is:
# 'Meta Data': {'1. Information': 'Intraday (5min) open, high, low, close prices and volume', '2. Symbol': 'WEED.TO', 
# '3. Last Refreshed': '2018-10-15 15:55:00', '4. Interval': '5min', '5. Output Size': 'Compact', '6. Time Zone': 'US/Eastern'}
# Second entry is a 100-entry dictionary of the 100 most recent 5-min periods:
# 'Time Series (5min)': {'2018-10-15 16:00:00': {'1. open': '73.4000', '2. high': '73.8800', '3. low': '73.4000', '4. close': '73.8800', '5. volume': '195788'}, '2018-10-15 15:55:00
# Each of the entries contains four floats and an integer

# path = 'data/*.ipynb'
# # path = '/home/ec2-user/weed_stocks/get_quotes/data/*.ipynb'
# # path = '/home/acer/weed_stocks/get_quotes/data/*.ipynb'
# files = glob.glob(path)   
# for fname in files: # 'file' is a builtin type, 'name' is a less-ambiguous variable name.
#     print('fname', fname)
#     str_data = open(fname).read()
#     json_data = json.loads(str_data)
#     # print(json_data['Meta Data'])
#     symbol=json_data['Meta Data']['2. Symbol']
#     # print('type(symbol)', type(symbol), 'symbol', symbol)
#     # cur.execute("INSERT IGNORE INTO symbol (symbol) VALUE (%s) ", (symbol,))
#     # print('here')
#     cur.execute('SELECT id FROM symbol WHERE symbol = (%s) ', (symbol,))
#     symbol_id = cur.fetchone()[0]
#     # print(json_data['Time Series (5min)'])
#     for period, values in json_data['Time Series (5min)'].items():
#         # print(period, values)
#         open_val = values['1. open']
#         high_val=values['2. high']
#         low_val=values['3. low']
#         close_val=values['4. close']
#         volume=values['5. volume']
#         tmp=datetime.datetime.strptime(period, "%Y-%m-%d %H:%M:%S")
#         per_unix=calendar.timegm(tmp.utctimetuple())
#         # print(tmp, per_unix)
#         # cur.execute('''INSERT IGNORE INTO Five_mins (five_min_start)
#         #     VALUES ( %s )''', ( per_unix, ) )
#         # cur.execute('SELECT id FROM Five_mins WHERE five_min_start = %s ', (per_unix, ))
#         # five_min_start_id = cur.fetchone()[0]
#         # print(symbol_id, five_min_start_id, open_val, high_val, low_val, close_val, volume)
#         cur.execute('''INSERT IGNORE INTO Symbol_five_mins(symbol_id, time_stamp, open, high, low, close, volume)
#             VALUES ( %s, %s, %s, %s, %s, %s, %s )''', ( symbol_id, per_unix, open_val, high_val, low_val, close_val, volume))
# # 
#     mydb.commit()

# SQL='''
# select min(time_stamp) as min_time_stamp, max(time_stamp) as max_time_stamp
# from Symbol_five_mins
# '''
# cur.execute(SQL)
# (min_time_stamp, max_time_stamp) = cur.fetchone()
# min_time_stamp_str = datetime.utcfromtimestamp(min_time_stamp).strftime('%Y-%m-%d %H:%M:%S')
# max_time_stamp_str = datetime.utcfromtimestamp(max_time_stamp).strftime('%Y-%m-%d %H:%M:%S')

# SQL = '''
# update Earliest_latest
# set earliest_5start = %s,
# earliest_5start_as_string = %s,
# latest_5start = %s,
# latest_5start_as_string = %s
# '''
# cur.execute(SQL, (min_time_stamp, min_time_stamp_str, max_time_stamp, max_time_stamp_str))

SQL = '''
select symbol from symbol
'''
cur.execute(SQL)
if cur.rowcount > 0:
    symbols = cur.fetchall()
    for symbol in symbols:
        print(symbol[0])
else:
    print("there is no symbols in the db")

mydb.commit()
cur.close()
mydb.close()