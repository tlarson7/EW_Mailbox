import Mailbox_Scrape
import inspect
from exchangelib import DELEGATE, Account, Credentials, Message, Mailbox
from Mailbox_Scrape import received_only, blanks_received, sent_CCIDs, blanks_sent
import sqlite3
import datetime
from Tanner_functions import print_len_label_val

cnxn = sqlite3.connect("EW_Review.db")
c = cnxn.cursor()

def convert_str_to_int(l):
    new_l = []
    for e in l:
        new_l.append(int(e))

    return new_l

# received_only = ['1005AD', '10087F', '100B45', '100B45', '100B46', '100CCC', '100DB8', '1015E9', '101837', '101838', 'F45E8', 'F4661', 'F4944', 'F4A50', 'F5090', 'F54DF', 'F54F8', 'F55A5', 'F5638', 'F5698', 'F572B', 'F5BE7', 'F6482', 'F69FF', 'F6B0C', 'F7263', 'F739C', 'F7A51', 'F7BB2', 'F7C76', 'F7D26', 'F7E4C', 'F80D9', 'F8180', 'F8386', 'F845A', 'F8873', 'F8BED', 'F8C4C', 'F8E36', 'F8F3A', 'F9117', 'F91E8', 'F9699', 'F97C3', 'F9EAF', 'FA15E', 'FA257', 'FA3C5', 'FA53A', 'FA61A', 'FA853', 'FA87C', 'FAC43', 'FB0FA', 'FB1AB', 'FB215', 'FB2E2', 'FB49E', 'FB751', 'FB7D0', 'FB9AB', 'FB9D8', 'FBBAF', 'FBC48', 'FBDC7', 'FBE70', 'FC173', 'FC837', 'FC914', 'FC945', 'FC9A5', 'FCCCA', 'FCE00', 'FCFB6', 'FD2EA', 'FD44E', 'FD560', 'FD6E1', 'FD7D4', 'FD945', 'FDC1A', 'FDF97', 'FDFDC', 'FE1E8', 'FE65D', 'FEAA7', 'FEAED', 'FEDEE', 'FF1A4', 'FF323', 'FF984', 'FFC77', 'No CCID Found']

# blanks_received = ['F739C', 'F7A51', 'F7BB2', 'F7C76', 'F845A', 'F8C4C', 'F8E36', 'F8F3A', 'F9117', 'FA3C5', 'FA53A', 'FB215', 'FBE70', 'FC837', 'FC914', 'FCCCA', 'FD2EA', 'FD44E', 'FD6E1', 'FD7D4', 'FD945', 'FE1E8', 'FEDEE', 'FF323', 'FF984', 'No CCID Found']

# sent_CCIDs = ['1001A3', '100349', '100A4A', '100CCB', '1010AD', '101487', '101839', '101BD6', '101C5F', '101E2C', '9E5', 'F49D1', 'F51C3', 'F5406', 'F55B4', 'F57FC', 'F5A60', 'F5FC2', 'F60F2', 'F7262', 'F7502', 'F7737', 'F77AC', 'F7837', 'F783A', 'F7F67', 'F8055', 'F8181', 'F81FA', 'F828E', 'F839D', 'F8CC8', 'F8F5E', 'F963C', 'F9672', 'F97A9', 'FA098', 'FA27F', 'FACF1', 'FADC4', 'FAF27', 'FB319', 'FB3A0', 'FB57A', 'FB9DF', 'FB9EC', 'FBB82', 'FBD04', 'FBD04', 'FBE5A', 'FC0A7', 'FC3F2', 'FC4B7', 'FC955', 'FCAF3', 'FD252', 'FD28B', 'FD452', 'FDCD5', 'FDCFA', 'FDD3E', 'FDDD6', 'FDDEE', 'FE076', 'FE71F', 'FF391', 'FFD49', 'FFE91']

# blanks_sent = []

check_contacts = []
unknown_issues = []
for CCID in received_only:
    if CCID in blanks_received:
        continue
    c.execute('SELECT Config_Status, AGR_End_Date, Num_Contacts FROM Config_Info WHERE CCID = ?',(CCID,))
    row = c.fetchone()

    if row[0] != "Active":
        continue
    if row[1] != None:
        date_str = row[1]
        date_str = date_str.split("-")
        date_str = convert_str_to_int(date_str)

        dt_obj = datetime.date(date_str[0], date_str[1], date_str[2])
        cur_date = datetime.date.today()
        if cur_date > dt_obj:
            continue

    num_contacts = int(row[2])
    if num_contacts == 0:
        check_contacts.append(CCID)
    else:
        unknown_issues.append(CCID)

print_len_label_val(check_contacts)
print_len_label_val(unknown_issues)

recheck_sent = []
for CCID in sent_CCIDs:
    if CCID in blanks_sent:
        continue
    c.execute('SELECT Config_Status, AGR_End_Date, Num_Contacts FROM Config_Info WHERE CCID = ?', (CCID,))
    row = c.fetchone()

    if row[0] != "Active":
        recheck_sent.append(CCID)
        continue

    if row[1] != None:
        date_str = row[1]
        date_str = date_str.split("-")
        date_str = convert_str_to_int(date_str)

        dt_obj = datetime.date(date_str[0], date_str[1], date_str[2])
        cur_date = datetime.date.today()
        if cur_date < dt_obj:
            continue

    recheck_sent.append(CCID)

print_len_label_val(recheck_sent)

cnxn.close()





