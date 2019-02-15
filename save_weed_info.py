import json, csv, datetime
from six.moves import urllib
# import urllib.request, re, time, os
import re, time, os
from subprocess import call

import mysql.connector 
mydb = mysql.connector.connect(
  # host="weeddb.cbdkoamqrvfd.us-west-2.rds.amazonaws.com",
  host="localhost",
  user="root",
  passwd="6617WoOD315!",
  database="symbol_prices",
  buffered=True
)
cur = mydb.cursor()

def write_file_to_disc(tr_sym, date_str=None):
    if date_str==None:
        date_str=datetime.datetime.today().strftime('%Y-%m-%d')
    address='https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=' + tr_sym + '&interval=5min&apikey=JN5MZQ7WGALU73D2'
    print('duh')
    uh = urllib.request.urlopen(address)
    print('duh2')

    data = uh.read()
    # print(data)
    info = json.loads(data.decode('utf-8'))
    if tr_sym=='N.V':
        print('type(info)', type(info), 'len(info)', len(info), 'info', info)
    if len(info)==1 and 'Error Message' in info and re.search('the parameter apikey is invalid or missin', info['Error Message']):
        print('API key: ' + tr_sym + ' invalid')
        return None

    if len(info)==1 and (('Information' in info and re.search('Alpha Vantage!', info['Information'])) or ('Note' in info and re.search('Alpha Vantage!', info['Note']))):
        print('Call to', tr_sym, 'Exceeded API calls.')
        time.sleep(60)
        uh = urllib.request.urlopen(address)
        data = uh.read()
        info = json.loads(data)
        # print('here', info)
        if len(info)==1 and 'Error Message' in info and re.search('the parameter apikey is invalid or missin', info['Error Message']):
            print('API key: ' + tr_sym + ' invalid')
            return None

    last_refreshed=info['Meta Data']['3. Last Refreshed']
    print(last_refreshed)
    # if re.search(date_str, last_refreshed) : # and (re.search('16:00:00', last_refreshed) or re.search('15:55:00', last_refreshed) or tr_sym=='SCU.TO') :
    print(tr_sym, 'last updated ',  last_refreshed) # 'today at 15:55:00 or 16:00:00 or this is SCU.TO')
    # with open('/home/acer/weed_stocks/get_quotes/data/' + tr_sym + '-' + date_str +'_evening.ipynb', 'w') as outfile:
    # with open('/home/ec2-user/weed_stocks/get_quotes/data/' + tr_sym + '-' + date_str +'.ipynb', 'w') as outfile:
    with open('/home/ubuntu/dana-weed-stocks/data/' + tr_sym + '-' + date_str +'.ipynb', 'w') as outfile:
    # with open('data/' + tr_sym + '-' + date_str +'.ipynb', 'w') as outfile:
        json.dump(info, outfile)
    # else:
    #   print(tr_sym, 'wasn\'t updated today at  15:55:00 or 16:00:00') # Improve this line. What if the symbol doesn't exist?
# # write_file_to_disc('gsghsjd##')
# write_file_to_disc('WEED.TO')
# # # write_file_to_disc('gsghsjd##')
# write_file_to_disc('TLRY') # TILRAY
# write_file_to_disc('SBUX') # Starbucks
# write_file_to_disc('SCU.TO') # Second Cup
# write_file_to_disc('HYYDF')
# # os.system("sleep(65)")
# write_file_to_disc('N.V')
# write_file_to_disc('HMMJ.TO')
# write_file_to_disc('CRON')
# try:
#     write_file_to_disc('APHA.TO')
# except:
#     print('Some problem w/ APHA.TO')
# write_file_to_disc('ACB.TO')
# # time.sleep(65)
# write_file_to_disc('TGODF') # Green Organic Dutchman Holdings Ltd
# write_file_to_disc('CNTTF') # CannTrust Holdings Inc
# write_file_to_disc('GTBIF') # Green Thumb Industries Inc
# write_file_to_disc('GWPH') # GW Pharmaceuticals PLC
# write_file_to_disc('ITHUF') # iAnthus Capital Holdings Inc
# # time.sleep(65)
# write_file_to_disc('MJNA') # Medical Marijuana Inc
# write_file_to_disc('MMNFF') #  MedMen Enterprises Inc. (OTC: MMNFF): up 36 percent
# write_file_to_disc('SMG') # Scotts Miracle-Gro Co (NYSE: SMG):
# write_file_to_disc('ZYNE') # Zynerba Pharmaceuticals Inc
# # time.sleep(65)
# write_file_to_disc('MICWF') # MicroWasteManagement - Also traded under another MCM.TO
# write_file_to_disc('HEXO.TO')

SQL = '''
select symbol from Symbol
'''
cur.execute(SQL)
if cur.rowcount > 0:
    symbols = cur.fetchall()
    for symbol in symbols:
        # print(symbol[0])
        write_file_to_disc(symbol[0])
else:
    print("there is no symbols in the db")

# # * This is the API's return when the nmber of calls has been exceeded:*<br>
# # {'Information': 'Thank you for using Alpha Vantage! Please visit https://www.alphavantage.co/premium/ if you would like to have a higher API call volume.'}<br><br>
# * The first argument when the call succeeds is : *<br>
# info["Meta Data"]<br>
# {'1. Information': 'Intraday (5min) open, high, low, close prices and volume',<br>
#  '2. Symbol': 'WEED.TO',<br>
#  '3. Last Refreshed': '2018-10-05 15:55:00',<br>
#  '4. Interval': '5min',<br>
# #  '5. Output Size': 'Compact',<br>
# #  '6. Time Zone': 'US/Eastern'}<br>
