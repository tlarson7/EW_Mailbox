# Testing SQL and github
import sqlite3
import pyodbc

cnxn = pyodbc.connect('DRIVER={SQL Server}; SERVER=connectwise; DATABASE=cwwebapp_eaglesoft; UID=expensewise; PWD=expensewise;')
c = cnxn.cursor()

c.execute('SELECT * FROM cwwebapp_eaglesoft.dbo.eagle_CV_configs_w_EW_agreements')
columns = [column[0] for column in c.description]
print(columns)
for row in c:
    print(row)