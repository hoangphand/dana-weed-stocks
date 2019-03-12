import json, csv, datetime
import re, time, os
import mysql.connector 
import numpy as np
from numpy import array

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="6617WoOD315!",
    database="symbol_prices",
    buffered=True
)

cur = mydb.cursor()

query = '''
SELECT symbol_id, date, high, volume 
FROM Symbol_daily
WHERE date BETWEEN DATE_SUB(NOW(), INTERVAL 90 DAY) AND NOW()
'''

dictData = {}
cur.execute(query)
if cur.rowcount > 0:
    rawData = cur.fetchall()

    listOfIds = []
    listOfDates = []

    for record in rawData:
        # ID
        if record[0] not in dictData:
            dictData[record[0]] = {}

        # Dates
        if record[1] not in listOfDates:
            listOfDates.append(record[1])

    # Init dictData
    for keyId in dictData:
        for date in listOfDates:
            dictData[keyId][str(date)] = np.nan

    # Fill dictData with real values
    for record in rawData:
        dictData[record[0]][str(record[1])] = record[2]
else:
    print("there is no symbols in the db")

arrayData = []
for i in range(0, len(dictData)):
    arrayData.append([])

    for keyDate in listOfDates:
        arrayData[i].append(dictData[i + 1][str(keyDate)])

numpyArray = array(arrayData)
maskedArray = np.ma.array(numpyArray, mask=np.isnan(numpyArray))
result = np.ma.corrcoef(maskedArray, rowvar=True, allow_masked=True).round(3)

for i in range(0, len(result)):
    print(result[i])

noOfIds = len(result)
for symbol1 in range(0, noOfIds):
    for symbol2 in range(0, noOfIds):
        if symbol1 != symbol2:
            # print("pair (" + str(symbol1) + ", " + str(symbol2) + ")")

            query = '''
            SELECT * FROM 3_months_correlation
            WHERE symbol1 = {0} AND symbol2 = {1}
            '''

            cur.execute(query.format(symbol1 + 1, symbol2 + 1))

            if cur.rowcount > 0:
                query = '''
                UPDATE 3_months_correlation
                SET corr = {0}
                WHERE symbol1 = {1} AND symbol2 = {2}
                '''

                cur.execute(query.format(result[symbol1][symbol2], symbol1 + 1, symbol2 + 1))
                mydb.commit()
            else:
                query = '''
                INSERT INTO 3_months_correlation(symbol1, symbol2, corr)
                VALUES ({0}, {1}, {2})
                '''

                cur.execute(query.format(symbol1 + 1, symbol2 + 1, result[symbol1][symbol2]))
                mydb.commit()
