from exchangelib import DELEGATE, Account, Credentials
from bs4 import BeautifulSoup
import inspect
import sqlite3
import datetime
import enchant

db_name = "EagleWatch"
cnxn = sqlite3.connect(f'/Users/TannerLarson/Desktop/SQLite Databases/{db_name}.db')
cnxn.row_factory = sqlite3.Row

e = enchant.Dict("en_US")

tanner_credentials = Credentials(username='eagle\\tanner',password='Jayhawks09')
EW_credentials = Credentials(username='eagle\\eaglewatch',password='3agleW@tch09')

my_account = Account(
    primary_smtp_address='tannerl@eagleinc.com',
    credentials=tanner_credentials,
    autodiscover=True,
    access_type=DELEGATE)

EW_account = Account(
    primary_smtp_address='eaglewatch@eagleinc.com',
    credentials=EW_credentials,
    autodiscover=True,
    access_type=DELEGATE)

def retrieve_name(var):
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is var]


def mod_retrieve_name(var):
    callers_local_vars = inspect.currentframe().f_back.f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is var]


def print_label_and_value(var):
    var_name = mod_retrieve_name(var)
    var_name = var_name[0]
    print(f"{var_name}:",var)


def get_CCID():
    el_list = soup.find_all(text=True)
    for el in el_list:
        if "CommCell ID" in el.text:
            # print("text:",el)
            el = el.split("CommCell ID:")[1]
            el = el.split("CommCell:")[0]
            CCID = el.strip()
            if "br" in CCID:
                CCID = CCID.strip("br")
            return CCID


def check_if_new_entry():
    new_entry_conditions = [
        len(columns) > 1,
        columns[0]["bgcolor"] != "#CCCCCC",
    ]

    if all(new_entry_conditions) == True:
        return True
    return False


def check_columns(d,tb_name):
    header_list = []
    column_list = []

    if type(d) == dict:
        for key in d.keys():
            header_list.append(key)
    elif type(d) == list:
        for item in d:
            header_list.append(item)
    # print("header_list:",header_list)

    c = cnxn.cursor()
    c.execute(f'SELECT * FROM "{tb_name}"')

    for column in c.description:
        column_list.append(column[0])
    # print(column_list)
    for header in header_list:
        if header.casefold() not in (col.casefold() for col in column_list):
            c.execute(f'ALTER TABLE "{tb_name}" ADD COLUMN "{header}" text')

    cnxn.commit()


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


def record_dict(d,tb_name):
    c = cnxn.cursor()
    c.execute(f'SELECT rowid, * FROM "{tb_name}"')
    rowid = c.lastrowid
    for key in d.keys():
        if d[key] == list:
            continue
        c.execute(f'UPDATE "{tb_name}" SET "{key}"=? WHERE rowid=?', (str(d[key]),main_rowid))

    cnxn.commit()


def record_job_data(d,sec_rowid):
    for key in d.keys():
        if type(d[key]) == list:
            tb_name = "Job Errors and Events"

            for item_i, item in enumerate(d[key]):
                if item_i > 0:
                    insert_null_row(tb_name)
                    sec_c.execute(f'SELECT rowid, * FROM "{tb_name}"')
                    sec_rowid = sec_c.lastrowid

                sec_c.execute(f'UPDATE "{tb_name}" SET "{key}"=?,"Main RowID"=? WHERE rowid="{sec_rowid}"',
                              (str(item), str(main_rowid)))

            cnxn.commit()

        if d[key] == []:
            continue
        tb_name = "EW Reports"
        record_var_in_last_row(d[key],key,tb_name)


def record_var_in_last_row(var,var_name,tb_name):
    c = cnxn.cursor()
    c.execute(f'SELECT rowid, * FROM "{tb_name}"')
    rowid = c.lastrowid
    c.execute(f'UPDATE "{tb_name}" SET "{var_name}"=? WHERE rowid=?', (str(var),main_rowid))
    cnxn.commit()


def check_if_end_entry():
    # TODO Beginning of table
    if current_row == "Table Name" or current_row == "Table Header" or current_row == "Row Header":
        return False

    if row_i+1 == len(rows):
        print("End of Table")
        return True
    next_row = rows[row_i+1]
    next_cols = next_row.find_all('td')
    if len(next_cols) > 1:
        return True
    return False


def get_emails_via_date():
    # start_date = datetime.datetime(2021, 9, 27, tzinfo=EW_account.default_timezone)
    # end_date = datetime.datetime(2021,9,30,tzinfo=EW_account.default_timezone)
    start_date = datetime.date.today()
    start_date = datetime.datetime(start_date.year,start_date.month,start_date.day,tzinfo=EW_account.default_timezone)
    end_date = datetime.date.today() + datetime.timedelta(days=1)
    end_date = datetime.datetime(end_date.year, end_date.month, end_date.day, tzinfo=EW_account.default_timezone)

    email_id_list = []
    emails = EW_account.inbox.filter(datetime_received__range=(start_date,end_date))
    for email in emails:
        print(email.id)
        if email.id not in sql_eID_list:
            email_id_list.append(email.id)
    return email_id_list


def get_emails_via_id(eID):
    email_id_list = []
    email = EW_account.inbox.get(id=eID)
    email_id_list.append(email.id)
    return email_id_list


def get_emails_via_sender(SA):
    email_id_list = []
    emails = EW_account.inbox.filter(sender=SA)[:1]
    for email in emails:
        print(email.id)
        email_id_list.append(email.id)
    return email_id_list


def get_eIDs_via_SQL():
    eID_list = []
    c = cnxn.cursor()
    c.execute(f'SELECT "Email ID" FROM "EW Reports"')
    for row in c:
        eID = row["Email ID"]
        if eID not in eID_list:
            eID_list.append(eID)
    return eID_list

# sql_eID_list = get_eIDs_via_SQL()
# email_id_list = get_emails_via_date()
email_id_list = get_emails_via_id("AAMkADU4NmEwYjI0LTVjODktNGEzZC05NGVmLTFkNjQ2MWJjYzAyNgBGAAAAAAAb3p6yFsc1TKAI7hgG4odfBwDzWQnoblRcQ6to91EQxs0aAAAAv3auAABxZ0PEvJynTZ//yIAeZma9AAP3RG0iAAA=")
# email_id_list = get_emails_via_sender("commvault@pngaming.com")

for email_id in email_id_list:
    email = EW_account.inbox.get(id=email_id)
    # print(email)
    # print(stuff.body)
    print(email.sender)
    email_id = email.id
    print(email_id)
    email_dt = email.datetime_received
    email_dt = str(email_dt)
    print(email_dt)
    dt = datetime.datetime.today().replace(microsecond=0)

    soup = BeautifulSoup(email.body,'html5lib')
    # print(soup.prettify())
    # quit()
    # print(soup.text)

    CCID = get_CCID()
    print_label_and_value(CCID)

    tables = soup.find_all("table")
    if len(tables) == 0 or email.attachments != []:
        # print(soup.prettify())
        insert_null_row("EW Reports")
        c = cnxn.cursor()
        c.execute(f'SELECT rowid, * FROM "EW Reports"')
        rowid = c.lastrowid
        main_rowid = rowid
        c.execute(f'UPDATE "EW Reports" SET "Tables not found"="YES" WHERE rowid="{rowid}"')
        c.execute(f'UPDATE "EW Reports" SET "Email ID"=? WHERE rowid="{rowid}"',(email_id,))
        c.execute(f'UPDATE "EW Reports" SET "CCID"=? WHERE rowid="{rowid}"',(CCID,))
        c.execute(f'UPDATE "EW Reports" SET "Email DT"=? WHERE rowid="{rowid}"',(email_dt,))
        c.execute(f'UPDATE "EW Reports" SET "Sender Address"=? WHERE rowid="{rowid}"', (str(email.sender.email_address),))
        record_var_in_last_row(dt,"DT Entered","EW Reports")
        record_var_in_last_row(main_rowid, "Main RowID", "EW Reports")

        cnxn.commit()
        print("=" * 200)
        continue

    # for table in tables:
    #     print(table.get_text())
    #     print("=" * 200)
    # quit()
    print("len(tables):", len(tables))
    if email.sender.email_address == 'Commvault@saracenresort.com':
        del tables[-3:]
    else:
        del tables[-1]
    print("len(tables):", len(tables))
    print("\n")
    # for table in tables:
    #     print(table.get_text())
    #     print("=" * 200)
    # quit()
    # print(tables[-1])
    # quit()

    for table in tables:
        table_headers = []
        table_name = ""
        row_headers = {}
        row_info = {}
        new_entry = False
        rows = table.find_all('tr')

        if len(rows) < 2:
            print("len(rows) < 2")
            continue
        # print("table.get_text():",table.get_text().strip())

        for row_i,row in enumerate(rows):
            current_row = None
            # print("row:",row)
            # print("\n")
            columns = row.find_all('td')
            # print("len(columns):",len(columns))
            # column_i = 0

            if len(columns) < 1:
                print("len(columns) < 1")
                continue

            # print(columns[0]["bgcolor"], len(columns))
            # continue
            try:
                meow = columns[0]["bgcolor"]
            except IndexError:
                columns[0]["bgcolor"] = None
            except KeyError:
                columns[0]["bgcolor"] = None
            new_entry = check_if_new_entry()
            if new_entry == True:
                # insert_null_row("EW Reports")
                row_headers = {}
                row_info = {}
                row_info["Failure Reason"] = []
                row_info["Associated Events"] = []
                row_info["Error Code"] = []

            for column_i,column in enumerate(columns):
                # print(column.get_text())
                column_text = column.get_text()

                try:
                    row_info["Color"] = column["bgcolor"]
                except KeyError:
                    row_info["Color"] = None
                    column["bgcolor"] = None
                    continue

                if len(columns) > 1:
                    if column["bgcolor"] == "#CCCCCC":
                        current_row = "Table Header"
                        str_table_header = column.get_text().replace("\n", " ")
                        str_table_header = str_table_header.strip()
                        table_headers.append(str_table_header)
                    else:
                        current_row = "Row Header"
                        lines = column.find_all('li')
                        if len(lines) > 0:
                            for line in lines:
                                text = line.get_text()
                                text = text.split(": ")
                                if len(text) < 2:
                                    continue

                                words = text[0].split(" ")
                                for word in words:
                                    if e.check(word) == True:
                                        if text[0] not in table_headers:
                                            table_headers.append(text[0])
                                        row_headers[text[0]] = text[1]
                                        break

                        try:
                            str_row_header = column.get_text().replace("\n"," ")
                            str_row_header = str_row_header.strip()
                            row_headers[table_headers[column_i]] = str_row_header
                        except IndexError:
                            continue
                else:
                    if column["bgcolor"] == "#000080":
                        current_row = "Table Name"
                        # print_label_and_value(row)
                        # print_label_and_value(row.get_text())
                        table_name = row.get_text()
                        table_name = table_name.strip()
                        # row_info["Table Name"] = table_name
                        # print_label_and_value(table_name)
                    else:
                        # text = row.get_text()#.strip()

                        lines = row.find_all('li')
                        for line_i,line in enumerate(lines):
                            text = line.get_text()
                            # print_label_and_value(line_i)
                            # print_label_and_value(text)

                            u_list = row.find_all('u')
                            for u in u_list:
                                u = u.get_text()
                                if u == "Failure Reason":
                                    if len(text) < 17:
                                        print("Probable issue with Failure Reason HTML")
                                        continue
                                    current_row = u

                                    row_info["Failure Reason"].append(text)
                                    row_info["Error Code"].append(text.split("]:")[0].split("[")[1])
                                    print("row_info['Error Code']:", row_info["Error Code"], "Color:",
                                          row_info["Color"])
                                #     TODO Add handler for getting source, job manager, etc.
                                elif u == "Associated Events":
                                    current_row = u
                                    row_info["Associated Events"].append(text.strip())
                                else:
                                    print("u not identified")

            if check_if_end_entry() == True:
                # print('len(row_info["Associated Events"]):', len(row_info["Associated Events"]))
                # print("\n")

                insert_null_row("EW Reports")
                c = cnxn.cursor()
                c.execute(f'SELECT rowid, * FROM "EW Reports"')
                main_rowid = c.lastrowid

                record_var_in_last_row(CCID, "CCID", "EW Reports")
                record_var_in_last_row(table_name, "Table Name", "EW Reports")
                record_var_in_last_row(email_id, "Email ID", "EW Reports")
                record_var_in_last_row(email_dt, "Email DT", "EW Reports")
                record_var_in_last_row(email.sender.email_address, "Sender Address", "EW Reports")
                record_var_in_last_row(dt, "DT Entered", "EW Reports")
                record_var_in_last_row(main_rowid, "Main RowID", "EW Reports")

                insert_null_row("Job Errors and Events")
                sec_c = cnxn.cursor()
                sec_c.execute(f'SELECT rowid, * FROM "Job Errors and Events"')
                sec_rowid = sec_c.lastrowid
                sec_c.execute(f'UPDATE "Job Errors and Events" SET "Main RowID"=? WHERE rowid=?',
                              (str(main_rowid), sec_rowid))

                check_columns(table_headers,"EW Reports")
                record_dict(row_headers,"EW Reports")
                record_job_data(row_info,sec_rowid)
                # dict_list = [table_headers, row_headers, row_info]
                # for dic in dict_list:
                #     check_columns(dic,"EW Reports")
                #     if type(dic) == dict:
                #         if dic != {}:
                #             record_job_data(dic)
                #             # record_dict(dic,"EW Reports")
        # print_label_and_value(table_headers)
    print("="*189)

cnxn.close()