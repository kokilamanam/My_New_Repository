

def holder_name():
    query = "SELECT Acc_holder,Acc_no from Account_info WHERE Acc_Holder =?"
    return query


def bank_customer_details():
    query = 'Select Cus_Id,Cus_Accno,Cus_Pn,cus_Branch from Customer_info where Cus_name=?'
    return query


def transaction_deposit():
    query = 'update  Account_info set Balance=Account_info.Balance+? where Acc_Holder=?'
    return query


def transaction_dpt():
    query = 'insert into Transaction_info(Tns_Account,Tns_Type,Tns_amount,createdat,createdby,modifiedat,modifiedby) values(?,?,?,?,?,?,?)'
    return query


def balance_method():
    query = 'Select Balance from Account_info where Acc_no=?'
    return query


def transaction_withD():
    query = 'update  Account_info set Balance=Account_info.Balance-? where Acc_Holder=?'
    return query


def transaction_wd():
    query = 'insert into Transaction_info(Tns_Account,Tns_Type,Tns_amount,createdat,createdby,modifiedat,modifiedby) values(?,?,?,?,?,?,?)'
    return query
