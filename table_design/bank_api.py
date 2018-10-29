"""IMPORTING REQUIRED MODULES"""
import datetime as dt
import os
from flask import Flask, jsonify, url_for, redirect
import pyodbc

app = Flask(__name__)

# "set up database connection to the sql server"


def conn_db():
    """creating method to connect db"""
    con = pyodbc.connect("Driver={ODBC Driver 11 for SQL Server};SERVER=cesdevsvr01\mssqldev; \
                         DATABASE=HBK_Test;UID=kokila;PWD=Prajju@123")
    cursor = con.cursor()
    return cursor


CURSOR = conn_db()

DATE = dt.datetime.now()
USER = os.getlogin()


# Account details
@app.route('/Acc_Holder/<name>')
def holder_name(name):
    """ creating method to get Account Details"""
    acc_object = get_holder_name(name)
    if acc_object:
        return redirect(url_for('customer_details', customername=name))
    return "Invalid Name ,Account not found"


def get_holder_name(name):
    """method for account holder details"""
    CURSOR.execute("SELECT Acc_holder,Acc_no from Account_info \
                    WHERE Acc_Holder =?", name)
    rows = CURSOR.fetchall()
    if rows:
        for row in rows:
            return row


# Customer details
@app.route('/Customer/<customername>')
def customer_details(customername):
    """ creating method to get customer Details"""
    cus_obj = get_customer_details(customername)
    if cus_obj:
        return jsonify({'Cus_Id': cus_obj[0], 'Cus_Accno': cus_obj[1],
                        'Cus_Pn': cus_obj[2], 'cus_Branch': cus_obj[3]})


def get_customer_details(customername):
    """creating customer method"""
    CURSOR.execute('Select Cus_Id,Cus_Accno,Cus_Pn,cus_Branch from Customer_info \
                     where Cus_name=?', customername)
    rows = CURSOR.fetchall()
    if rows:
        for row in rows:
            return row


# Transactions Details
@app.route('/Transaction/<name>/<tns_account>/<tns_type>/<amount>')
def transaction_details(name, tns_account, tns_type, amount):
    """ creating method to get Transaction Details"""
    if tns_type == 'deposit':
        CURSOR.execute('update  Account_info set Balance=Account_info.Balance+? \
                        where Acc_Holder=?', amount, name)
        CURSOR.commit()
        CURSOR.execute('insert into Transaction_info(Tns_Account,Tns_Type,Tns_amount,createdat,\
        createdby,modifiedat,modifiedby) values(?,?,?,?,?,?,?)',
        tns_account, tns_type, amount, DATE, USER, DATE, USER)
        CURSOR.commit()
        return "Amount deposited"

    if tns_type == 'Withdraw':
        balance = get_balance(tns_account)
        if float(amount) > float(balance[0]):
            return "Insufficient Balance"

        CURSOR.execute('update  Account_info set Balance=Account_info.Balance-? \
                                where Acc_Holder=?', amount, name)
        CURSOR.commit()
        CURSOR.execute('insert into Transaction_info(Tns_Account,Tns_Type,Tns_amount,createdat,\
        createdby,modifiedat,modifiedby) values(?,?,?,?,?,?,?)',
        tns_account, tns_type, amount, DATE, USER, DATE, USER)
        CURSOR.commit()
        return " Amount withdrawn successfully"
    return "Thank you"


def get_balance(tns_account):
    """"creating balance method"""
    CURSOR.execute('Select Balance from Account_info \
                   where Acc_no=?', tns_account)
    rows = CURSOR.fetchall()
    if rows:
        for row in rows:
            return row


app.run(debug=True)

