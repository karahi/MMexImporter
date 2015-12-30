'''
@author: ssuppe
'''

from mmeximporter import MMexDB, Settings
import util
import sys, os
import csv
import datetime

def format_date(date):
  return date.strftime("%Y-%m-%d")

settings = Settings.Settings()

account_number = sys.argv[1]
file_to_import = sys.argv[2]

# Get sample of file
if not os.path.isfile(file_to_import):
  print "File '%s' does not exist." % (file_to_import)
  print "Usage: mmeximporter.py <account_number> <file_to_import>"
  sys.exit(-1)

confirm = util.query_yes_no("Importing %s into account: %s, ready?" % (file_to_import, account_number))
if not confirm:
  sys.exit(-1)


db = MMexDB.MMexDb(settings)
# transactions = db.get_transactions(account_number)
# print transactions

reader = csv.reader(open(file_to_import, "r"))
schema = settings.getSchema(account_number)

if schema['header']:
  reader.next()
  
if schema['inverse_amount']:
  m = -1
else:
  m = 1
  
DATE = schema["date"]
DATE_FORMAT = schema['date_format']

for row in reader:
  TRANSID = None
  ACCOUNTID = db.get_accountid(account_number)
  TOACCOUNTID = -1
  
  # Check if Payee exists in the DB, otherwise create
  PAYEE = row[schema['payee']]
  PAYEEID = db.register_payeeid(PAYEE)
  print "PAYEE ID: ", PAYEEID
  # Transactions are stored as absolute values and defined as withdrawals/deposits.
  TRANSAMOUNT = float(row[schema["amount"]])*m
  if TRANSAMOUNT < 0:
    TRANSCODE = "Withdrawal"
  else:
    TRANSCODE = "Deposit"
  TRANSAMOUNT = abs(TRANSAMOUNT)
  STATUS = ""
  if 'transaction_number' in schema:
    TRANSACTIONNUMBER = row[schema['transaction_number']]
  else:
    TRANSACTIONNUMBER = None

  if 'notes' in schema:
    NOTES = row[schema['notes']]
  else:
    NOTES = None

  CATEGID = -1
  SUBCATEGID = -1
  TRANSDATE = format_date(datetime.datetime.strptime(row[schema['date']], DATE_FORMAT))
  FOLLOWUPID = -1
  TOTRANSAMOUNT = TRANSAMOUNT
 
  t = db.search_transaction(ACCOUNTID=ACCOUNTID, PAYEEID=PAYEEID, TRANSAMOUNT=TRANSAMOUNT, TRANSDATE=TRANSDATE)
  confirm = True
  if t:
    print "%s - %s : %s (%s)" % (TRANSDATE, PAYEE, TRANSAMOUNT, TRANSCODE)
    confirm = util.query_yes_no("A possible Transaction already exists. Do you want to continue?", default="no")

  if confirm: 
    t = db.save_transaction(TRANSID = TRANSID, ACCOUNTID=ACCOUNTID, TOACCOUNTID=TOACCOUNTID, PAYEEID=PAYEEID, TRANSAMOUNT=TRANSAMOUNT,  TRANSCODE=TRANSCODE, STATUS=STATUS, TRANSACTIONNUMBER=TRANSACTIONNUMBER, NOTES=NOTES, CATEGID=CATEGID, SUBCATEGID=SUBCATEGID, TRANSDATE=TRANSDATE, FOLLOWUPID=FOLLOWUPID, TOTRANSAMOUNT=TOTRANSAMOUNT)
