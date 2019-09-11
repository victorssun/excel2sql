# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 20:37:12 2019

@author: A
"""

import mysql.connector
import datetime
import dateutil.relativedelta
import pandas as pd

def opensql():
    # open sql
    connection = mysql.connector.connect(host='localhost', database='expenses', user='user', password='password')
    cursor = connection.cursor()
    return connection, cursor

def openexcel():
    # open excel
    file_excel = r'PATH\Monthly Spending.xlsm'
    xl = pd.ExcelFile(file_excel)
    sheet_names = xl.sheet_names 
    return file_excel, sheet_names

def sortdata(df):
    list_trans = []
    for i in range(len(df)):
        if df.iloc[i,0] == 'Description': # if first col has header, call it card 1 with appriopiate PC cols, and skip rest of loop (this assumes card 1 spreadsheet is placed first)
            card = 'card 1'
            col_date_trans = 3
            col_merchant = 0
            continue
        elif df.iloc[i,0] == 'Transaction date': # if first col has header, call it card 2 with appr. tangerine cols, dont skip (this assumes card 2 spreadsheet is overlapping with another transaction)
            card = 'card 2'
            col_date_trans = 0
            col_merchant = 2
        elif pd.isna(df.iloc[i,0]):
            card = None
        # if amount col is empty, skip loop
        if pd.isna(df.iloc[i,7]):
            continue
        # if merchant col is empty, call it None
        if pd.isna(df.iloc[i, col_merchant]):
            merch = None
        else:
            merch = df.iloc[i, col_merchant]
        # try to input transaction date, if fail, call transaction date None, merchant None, card None
        isTrue = False
        try:
            date_trans = datetime.datetime.strptime(df.iloc[i, col_date_trans], '%m/%d/%Y').date()
        except:
            date_trans = None
            merch = None
            card_temp = card
            card = None
            isTrue = True
            
        temp = (df.iloc[i,7], df.iloc[i,6], month, date_trans, merch, card) # amount, category, date_month, date_trans, merchant, card
        if isTrue == True: # return card back to previous card label
            card = card_temp
        list_trans.append(temp) 
    return list_trans

def list2sql(list_trans):
    # insert data
    sql = 'INSERT INTO transactions (amount, category, date_month, date_transaction, merchant, card) VALUES (%s, %s, %s, %s, %s, %s)'
    val = list_trans
    cursor.executemany(sql, val)
    
    # commit to db
    connection.commit()
    print(cursor.rowcount, "was inserted.") 
    return 

### MAIN ###
connection, cursor = opensql()
file_excel, sheet_names = openexcel() # find appriopiate sheet name
month = datetime.date(2019, 9, 1) # month of, even though it says the first
month_sheet = sheet_names[5] # input number

df = pd.read_excel(file_excel, sheet_name=xl.sheet_names[j], header=None)
list_trans = sortdata(df)
list2sql(list_trans)

# check it was added correctly
sql = 'SELECT * FROM transactions ORDER BY id DESC LIMIT %s'
val = cursor.rowcount + 5
cursor.execute(sql, val)
output = cursor.fetchall()
for x in output:
    print(x)
    
    
# close
cursor.close() # close sql cmds
connection.close() # close sql connection

