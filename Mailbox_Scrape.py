from exchangelib import DELEGATE, Account, Credentials, Message, Mailbox
from bs4 import BeautifulSoup
import inspect
import datetime
from Tanner_functions import print_len_label_val

EW_credentials = Credentials(username='eagle\\eaglewatch',password='uOTc22tGZT75cFK1x^F!Cd&ZTs5ET8')

EW_account = Account(
    primary_smtp_address='eaglewatch@eagleinc.com',
    credentials=EW_credentials,
    autodiscover=True,
    access_type=DELEGATE)

Support_credentials = Credentials(username="voicemail4support",password="x*xTx79snPUSyW$DNYZ@SxxX$JR2R3")

Support_account = Account(
    primary_smtp_address='Support@eagleinc.com',
    credentials=Support_credentials,
    autodiscover=True,
    access_type=DELEGATE
)

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

def get_CCID_from_sent():
    el_list = soup.find_all(text=True)
    for el in el_list:
        if "ccID" in el.text:
            # print("text:",el)
            el = el.split("ccID:")[1]
            el = el.split("Version:")[0]
            CCID = el.strip()
            if "br" in CCID:
                CCID = CCID.strip("br")
            return CCID

def get_emails_via_date():
    # start_date = datetime.datetime(2022, 2, 11, tzinfo=EW_account.default_timezone)
    start_date = datetime.date.today() - datetime.timedelta(days=1)
    # end_date = datetime.datetime(2021,9,30,tzinfo=EW_account.default_timezone)

    # start_date = datetime.date.today()
    start_date = datetime.datetime(start_date.year,start_date.month,start_date.day,tzinfo=EW_account.default_timezone)
    end_date = datetime.date.today() + datetime.timedelta(days=1)
    end_date = datetime.datetime(end_date.year, end_date.month, end_date.day, tzinfo=EW_account.default_timezone)

    email_id_list = []
    emails = EW_account.inbox.filter(datetime_received__range=(start_date,end_date))
    for email in emails:
        print(email.id)
        # if email.id not in sql_eID_list:
        email_id_list.append(email.id)
    return email_id_list

def get_sent_emails():
    # start_date = datetime.datetime(2022, 2, 11, tzinfo=Support_account.default_timezone)
    start_date = datetime.date.today() - datetime.timedelta(days=1)
    # end_date = datetime.datetime(2021,9,30,tzinfo=Support_account.default_timezone)

    # start_date = datetime.date.today()
    start_date = datetime.datetime(start_date.year, start_date.month, start_date.day,tzinfo=Support_account.default_timezone)
    end_date = datetime.date.today() + datetime.timedelta(days=1)
    end_date = datetime.datetime(end_date.year, end_date.month, end_date.day, tzinfo=Support_account.default_timezone)

    email_id_list = []
    emails = Support_account.sent.filter(datetime_sent__range=(start_date, end_date))
    for email in emails:
        print(email.id)
        # if email.id not in sql_eID_list:
        email_id_list.append(email.id)
    return email_id_list

def convert_list_to_string(l):
    new_str = ""
    l.sort()
    for item in l:
        new_str += item + ", "
    return new_str

# =====================================================
email_id_list = get_emails_via_date()
received_CCIDs = []
sent_CCIDs = []
blanks_received = []
received_only = []
duplicates_sent = []
blanks_sent = []

for email_id in email_id_list:
    email = EW_account.inbox.get(id=email_id)
    # print(email)
    print(email.sender)
    email_id = email.id

    soup = BeautifulSoup(email.body, 'html5lib')
    # print(soup.prettify())
    # print(soup.text)

    CCID = get_CCID()
    print_label_and_value(CCID)
    if CCID == None:
        CCID = "No CCID Found"
    received_CCIDs.append(CCID)

    ### Check if report is blank via number of tables
    tables = soup.find_all("table")
    if len(tables) == 0 or email.attachments != []:
        blanks_received.append(CCID)

send_id_list = get_sent_emails()
for sent_id in send_id_list:
    email = Support_account.sent.get(id=sent_id)
    print(email.subject)

    if "EAGLEWatchWeek" not in email.subject:
        continue

    soup = BeautifulSoup(email.body, 'html5lib')
    # print(soup.prettify())
    # print(soup.text)

    CCID = get_CCID_from_sent()
    print_label_and_value(CCID)
    sent_CCIDs.append(CCID)

    tables = soup.find_all("table")
    if len(tables) == 0 or email.attachments != []:
        blanks_sent.append(CCID)

for rec_id in received_CCIDs:
    if rec_id not in sent_CCIDs:
        received_only.append(rec_id)

for sID in set(sent_CCIDs):
    if sent_CCIDs.count(sID) > 1:
        duplicates_sent.append(sID)

received_CCIDs.sort()
sent_CCIDs.sort()
blanks_received.sort()
received_only.sort()
duplicates_sent.sort()
blanks_sent.sort()

print_len_label_val(received_CCIDs)
print_len_label_val(sent_CCIDs)
print_len_label_val(blanks_received)
print_len_label_val(received_only)
print_len_label_val(duplicates_sent)
print_len_label_val(blanks_sent)


received_CCIDs_string = convert_list_to_string(received_CCIDs)
sent_CCIDs_string = convert_list_to_string(sent_CCIDs)

subject_string = "EW Review " + str(datetime.datetime.today().date())

body_string = "Emails Received: " + str(len(received_CCIDs)) + "\n" + "CCIDs: " + "\n" + received_CCIDs_string + "\n" + "\n" + "Emails Sent: " + str(len(sent_CCIDs)) + "\n" + "CCIDs: " + "\n" + sent_CCIDs_string

m = Message(
    account=EW_account,
    subject=subject_string,
    body=body_string,
    to_recipients=['tannerl@eagleinc.com']
)
# m.send()
