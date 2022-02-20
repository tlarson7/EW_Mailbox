import Mailbox_Scrape
import sqlite3
import datetime

def insert_null_row(tb_name):
    c = cnxn.cursor()
    c.execute(f'SELECT * FROM "{tb_name}"')
    Qmarks = ""
    Nullist = []
    for i in c.description:
        Qmarks = Qmarks + "?,"
        Nullist.append(None)
    Qmarks = Qmarks.strip(Qmarks[-1])
    c.execute(f'INSERT INTO "{tb_name}" VALUES ({Qmarks})', Nullist)

    cnxn.commit()

def record_var_in_last_row(var,var_name,tb_name):
    c = cnxn.cursor()
    c.execute(f'SELECT rowid, * FROM "{tb_name}"')
    rowid = c.lastrowid
    c.execute(f'UPDATE "{tb_name}" SET "{var_name}"=? WHERE rowid=?', (str(var),rowid))
    cnxn.commit()

def update_records(l,action):
    c = cnxn.cursor()
    # d = datetime.date.today()
    d = datetime.date.today() - datetime.timedelta(days=1)
    for e in l:
        if e == "No CCID Found":
            continue
        c.execute('INSERT INTO Report_History VALUES (?,?,?)',(e,d,action))

    cnxn.commit

#     ================================================

cnxn = sqlite3.connect("EW_Review.db")
c = cnxn.cursor()

CCIDs_sqlite = []
c.execute('SELECT "CCID" FROM "Config_Info"')
for row in c:
    CCIDs_sqlite.append(row[0])

for report_CCID in set(Mailbox_Scrape.received_CCIDs):
    if report_CCID not in CCIDs_sqlite:
        if report_CCID == "No CCID Found":
            continue
        insert_null_row("Config_Info")
        record_var_in_last_row(report_CCID,"CCID","Config_Info")

update_records(set(Mailbox_Scrape.received_only),"Received")
update_records(set(Mailbox_Scrape.sent_CCIDs),"Sent")


cnxn.commit()
cnxn.close()