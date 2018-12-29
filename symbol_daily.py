import json, csv, datetime
from six.moves import urllib
# import urllib.request, re, time, os
import re, time, os
from subprocess import call
import mysql.connector 

mydb = mysql.connector.connect(
	host="localhost",
	user="root",
	passwd="6617WoOD315!",
	database="symbol_prices",
	buffered=True
)

cur = mydb.cursor()

api_key = 'JN5MZQ7WGALU73D2'
api_function = 'TIME_SERIES_DAILY'
api_compact_url = 'https://www.alphavantage.co/query?function={0}&symbol={1}&interval=5min&apikey={2}'
api_full_url = 'https://www.alphavantage.co/query?function={0}&symbol={1}&interval=5min&apikey={2}&outputsize=full'

query = '''
select id, symbol from Symbol
'''

cur.execute(query)
if cur.rowcount > 0:
	symbols = cur.fetchall()
	temp_query = '''insert ignore into Symbol_daily(symbol_id, date, open, low, high, close, volume) 
		values ({0}, '{1}', {2}, {3}, {4}, {5}, {6})'''

	for symbol in symbols:
		api_call_string = api_full_url.format(api_function, symbol[1], api_key)
		api_request = urllib.request.urlopen(api_call_string)

		raw_data = api_request.read()
		json_data = json.loads(raw_data.decode('utf-8'))

		if 'Meta Data' not in json_data:
			print(json_data['Note'])
			print('sleeping...')

			time.sleep(60)

			api_request = urllib.request.urlopen(api_call_string)

			raw_data = api_request.read()
			json_data = json.loads(raw_data.decode('utf-8'))

		print(json_data['Meta Data']['2. Symbol'])

		price_data = json_data['Time Series (Daily)']

		for date in price_data:
			open_val = price_data[date]['1. open']
			high_val = price_data[date]['2. high']
			low_val = price_data[date]['3. low']
			close_val = price_data[date]['4. close']
			volume_val = price_data[date]['5. volume']

			insert_query = temp_query.format(symbol[0], date, open_val, low_val, high_val, close_val, volume_val)
			cur.execute(insert_query)

		mydb.commit()
else:
	print("there is no symbols in the db")

