"""IMPORTING REQUIRED MODULES"""
import datetime as dt
import os
import db_conn
import queries
from flask import Flask, json, url_for, redirect


app = Flask(__name__)
# setting up the database connection


CURSOR = db_conn.conn_db()

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
    CURSOR.execute(queries.holder_name(), name)
    rows = CURSOR.fetchall()
    if len(rows) == 1:
        return rows[0]


# Customer details
@app.route('/Customer/<customername>')
def customer_details(customername):
    """ creating method to get customer Details"""
    cus_obj = get_customer_details(customername)
    if cus_obj:
        return json.dumps({'Cus_Id': cus_obj[0], 'Cus_Accno': cus_obj[1],
                        'Cus_Pn': cus_obj[2], 'cus_Branch': cus_obj[3]})


def get_customer_details(customername):
    """creating customer method"""
    CURSOR.execute(queries.bank_customer_details(), customername)
    rows = CURSOR.fetchall()
    if len(rows) == 1:
        return rows[0]


# Transactions Details
@app.route('/Transaction/<name>/<tns_account>/<tns_type>/<amount>')
def transaction_details(name, tns_account, tns_type, amount):
    """ creating method to get Transaction Details"""
    try:
            if tns_type == 'deposit':
                CURSOR.execute(queries.transaction_deposit(), amount, name)
                CURSOR.commit()
                CURSOR.execute(queries.transaction_dpt(), tns_account, tns_type, amount, DATE, USER, DATE, USER)
                CURSOR.commit()
                return "Amount deposited"

            if tns_type == 'Withdraw':
                balance = get_balance(tns_account)
                if float(amount) > float(balance[0]):
                    return "Insufficient Balance"
                CURSOR.execute(queries.transaction_withD(), amount, name)
                CURSOR.commit()
                CURSOR.execute(queries.transaction_wd(), tns_account, tns_type, amount, DATE, USER, DATE, USER)
                CURSOR.commit()
                return " Amount withdrawn successfully "
            return "not_found()"

    except Exception as e:
          print(e)


def get_balance(tns_account):
    """"creating balance method"""
    CURSOR.execute(queries.balance_method(), tns_account)
    rows = CURSOR.fetchall()
    if rows:
        for row in rows:
            return row


app.run(debug=True)
