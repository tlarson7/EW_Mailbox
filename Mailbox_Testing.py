from exchangelib import DELEGATE, Account, Credentials, Message, Mailbox
from bs4 import BeautifulSoup
import inspect
import datetime

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

# start_date = datetime.date.today()
# start_date = datetime.datetime(start_date.year,start_date.month,start_date.day,tzinfo=EW_account.default_timezone)
# start_date = datetime.datetime(2022, 2, 7, tzinfo=EW_account.default_timezone)
# end_date = datetime.date.today() + datetime.timedelta(days=1)
# end_date = datetime.datetime(end_date.year, end_date.month, end_date.day, tzinfo=EW_account.default_timezone)
#
# # emails = Support_account.sent.all()[:1]
# emails = Support_account.sent.filter(datetime_sent__range=(start_date,end_date))
# for email in emails:
#     print(email.subject)

### Message testing
m = Message(
    account=EW_account,
    subject="EW Review",
    body="Meow",
    to_recipients=['tannerl@eagleinc.com']
)
m.send()