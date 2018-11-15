"""IMPORTING REQUIRED MODULES"""
import datetime as dt
import os
import db_conn
import queries
from flask import Flask, json, url_for, redirect, request, jsonify, Response


app = Flask(__name__)
# setting up the database connection


CURSOR = db_conn.conn_db()

DATE = dt.datetime.now()
USER = os.getlogin()


# Account details
@app.route('/Acc_Holder/<name>/<password>')
def holder_name(name, password):
    """ creating method to get Account Details """
    acc_object = get_holder_name(password)
    if acc_object:
        return redirect(url_for('customer_details', customername=name))
    # return "Invalid password ,{} Account not found".format(name)
    return redirect(url_for('adding_user', code=307))

def get_holder_name(password):
    """method for account holder details"""
    CURSOR.execute(queries.holder_name(), password)
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
                return ".....Amount deposited....."

            if tns_type == 'Withdraw':
                balance = get_balance(tns_account)
                if float(amount) > float(balance[0]):
                    return "Insufficient Balance"
                CURSOR.execute(queries.transaction_withD(), amount, name)
                CURSOR.commit()
                CURSOR.execute(queries.transaction_wd(), tns_account, tns_type, amount, DATE, USER, DATE, USER)
                CURSOR.commit()
                return " .......Amount withdrawn successfully....... "
            return "not_found()"

    except Exception as e:
          print(e)
          return "not_found"


def get_balance(tns_account):
    """"creating balance method"""
    CURSOR.execute(queries.balance_method(), tns_account)
    rows = CURSOR.fetchall()
    if rows:
        for row in rows:
            return row


#for Adding customers
@app.route('/add_u', methods=['POST'])
def adding_user():
    """Adding new Customers....."""
    try:
        _json = request.json
        Acc_Holder = _json['Acc_Holder']
        Acc_no = _json['Acc_no']
        Acc_type = _json['Acc_type']
        Balance = _json['Balance']
        Branch = _json['Branch']
        createdat = DATE
        createdby = _json['USER']
        modifiedat = DATE
        modifiedby = _json['USER']
        password = _json['password']

        if request.method == 'POST':
            CURSOR.execute(queries.adding_details(), Acc_Holder, Acc_no, Acc_type, Balance, Branch, createdat,
                           createdby, modifiedat, modifiedby, password)
            CURSOR.commit()
            # return "customer details added....."
            # resp = jsonify('User added successfully!')
            # resp.status_code = 200
            return Response('File Updated successfully', status=200)
        return 'not_found()'

    # except KeyError as ke:
    #     print(ke)
    #     return str(ke)
    except Exception as e:
        print(e)
        return 'DB error'


@app.route('/user/<password>')
def user(password):
    """Reading customer details"""
    try:
        if request.method == 'GET':
                CURSOR.execute(queries.read_details(), password)
                row = CURSOR.fetchall()
                resp = json.dumps(row)
                print(resp)
                resp.status_code = 200
                return resp
        return 'not_found()'

    except Exception as e:
            print(e)
            return 'DB error'

app.run(debug=True)
