import pyodbc, datetime as dt, os

# con = pyodbc.connect('Driver={ODBC Driver 11for SQL Server};server=cesdevsvr01\mssqldev;database=HBK_Test;user=kokila;password=Welcome@123;')
con = pyodbc.connect('Driver={ODBC Driver 11 for SQL Server};SERVER=cesdevsvr01\mssqldev;DATABASE=HBK_Test;UID=kokila;PWD=Prajju@123')
cursor = con.cursor()


# bank = 'create table Bank_info([Bank_name] nvarchar(20),[Branch] nvarchar(20),IFSC_code int )'
# cursor.execute(bank)


# acc = 'create table Account_info(Acc_Holder nvarchar(20), [Acc_no] int primary key,[Acc_Type] nvarchar(20),Balance float,Branch nvarchar(15),\
#                                   createdat datetime,createdby nvarchar(20),modifiedat datetime,modifiedby nvarchar(20))'
# cursor.execute(acc)


# customer = 'create table Customer_info(Cus_Id int primary key,cus_name nvarchar(20),\
#             Cus_Accno int Foreign key references Account_info([Acc_no]),Cus_Pn int,cus_Branch nvarchar(20),\
#             createdat datetime,createdby nvarchar(20),modifiedat datetime,modifiedby nvarchar(20))'
# cursor.execute(customer)

tranc = 'create table Transaction_info(Tns_ID int Identity(100,101),Tns_Account int Foreign key references Account_info([Acc_no]), \
                                        Tns_Type nvarchar(20),Tns_amount float,\
                                       createdat datetime,createdby nvarchar(20),modifiedat datetime,modifiedby nvarchar(20))'
cursor.execute(tranc)


date = dt.datetime.now()
user = os.getlogin()
#
# bk = 'INSERT into Bank_info(Bank_name,Branch,IFSC_code) values (?,?,?)'
# data = [('ICICI', 'gowlidoddi', '000567'),
#         ('SBI', 'KPHB', '000145'), ('ANDHRA', 'KPHB', '000763')]
# cursor.executemany(bk, data)

# act = 'INSERT into Account_info(Acc_Holder,Acc_no,Acc_Type,Balance,Branch,createdat,createdby,modifiedat,modifiedby) values(?,?,?,?,?,?,?,?,?)'
# info = [('Ajay', '123', 'savings', 1000, 'KPHB', date, user, date, user),
#        ('priya', '456', 'current', 2000, 'KPHB', date, user, date, user),
#        ('Nani', '789', 'savings', 2500, 'gowlidoddi',date, user, date, user)]
# cursor.executemany(act, info)
#
# cus = 'INSERT into Customer_info(Cus_Id,cus_name,Cus_Accno,Cus_pn,Cus_Branch,createdat,createdby,modifiedat,modifiedby) values(?,?,?,?,?,?,?,?,?)'
# inf = [(400, 'Ajay', 123, 95012, 'kphb', date, user, date, user),
#         (401, 'priya', 456, 96734, 'kphb', date, user, date, user),
#         (402, 'Nani', 789, 96023, 'gowlidoddi', date, user, date, user)]
# cursor.executemany(cus, inf)

#
# tns = 'INSERT into Transaction_info(Tns_ID,Tns_Type,Tns_amount,Tns_acc,createdat,createdby,modifiedat,modifiedby) values(?,?,?,?,?,?,?,?)'
# infom=[(501, '', '', '123', date, user, date, user),
#        (502, '', '', '456', date, user, date, user),
#        (503, '', '', '789', date, user, date, user)]
# cursor.executemany(tns, infom)


con.commit()



