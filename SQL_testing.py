# Testing SQL and github
import sqlite3
import pyodbc

def update_row():
    cursor_sqlite_execute.execute('UPDATE Config_Info SET Config_Status = ?, AGR_End_Date = ?, Cancelled_Flag = ?, Company_Name = ?, Num_Contacts = ? WHERE CCID = ?',(status,end_date,cancelled,company,num_contacts,CCID))

    cnxn_sqlite.commit()

cnxn_MySQL = pyodbc.connect('DRIVER={SQL Server}; SERVER=connectwise; DATABASE=cwwebapp_eaglesoft; UID=expensewise; PWD=expensewise;')
cnxn_MySQL2 = pyodbc.connect('DRIVER={SQL Server}; SERVER=connectwise; DATABASE=cwwebapp_eaglesoft; UID=expensewise; PWD=expensewise;')
cursor_agr_view = cnxn_MySQL.cursor()
cursor_contact_view = cnxn_MySQL2.cursor()

cnxn_sqlite = sqlite3.connect("EW_Review.db")
cursor_sqlite_select = cnxn_sqlite.cursor()
cursor_sqlite_execute = cnxn_sqlite.cursor()

cursor_agr_view.execute('SELECT "Config_Name","Description","AGR_Date_End","AGR_Cancel_Flag","Company_Name" FROM cwwebapp_eaglesoft.dbo.eagle_CV_configs_w_EW_agreements')
# columns = [column[0] for column in cursor_agr_view.description]
# print(columns)
for row in cursor_agr_view:
    config_name = row[0] #TODO Check if same as Contact view
    status = row[1]
    end_date = row[2]
    cancelled = row[3]
    company = row[4]

    cursor_contact_view.execute('SELECT "Email_Flag" FROM cwwebapp_eaglesoft.dbo.eagle_EW_CV_Contacts WHERE "Config_Name" = ?',(config_name))
    num_contacts = len(cursor_contact_view.fetchall())
    print(config_name,"|",status,"|",end_date)

    #TODO Add initial select check so not to add unneeded loop
    cursor_sqlite_select.execute('SELECT "CCID" FROM "Config_Info" WHERE CCID = ?',(config_name,))
    if len(cursor_sqlite_select.fetchall()) == 1:
        cursor_sqlite_select.execute('SELECT "CCID" FROM "Config_Info" WHERE CCID = ?', (config_name,))
        for row_sqlite in cursor_sqlite_select:
            CCID = row_sqlite[0]
        update_row()

    else:
        print("Starting Else")
        cursor_sqlite_select.execute('SELECT "CCID" FROM "Config_Info"')
        for row_sqlite in cursor_sqlite_select:
            CCID = row_sqlite[0]
            if CCID.casefold() in config_name.casefold():
                update_row()

