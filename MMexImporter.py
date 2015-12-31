'''
@author: ssuppe
'''

from mmeximporter import MMexDB, Settings, UserError
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

reader = csv.reader(open(file_to_import, "r"))
schema = settings.getSchema(account_number)

categories = settings.getCategories()

if 'header' in schema and schema['header'] == "True":
  reader.next()
  
DATE = schema["date"]
DATE_FORMAT = schema['date_format']

for row in reader:
  TRANSID = None
  ACCOUNTID = db.get_accountid(account_number)
  TOACCOUNTID = -1
  
  # Check if Payee exists in the DB, otherwise create
  if 'payee' in schema:
    try:
      PAYEE = row[schema['payee']]
    except IndexError as e:
      print "Row:", row
      raise
    PAYEEID = db.register_payeeid(PAYEE)
  else:
    raise UserError.UserError("Payee is missing from configuration")
    
  if "amount" in schema:
    # Transactions are stored as absolute values and defined as withdrawals/deposits. 
    # We then allow the user to 'flip the sign' (since MMeX requires withdrawals to be negative
    
    if 'inverse_amount' in schema and schema['inverse_amount'] == "True":
      m = -1
    else:
      m = 1
    TRANSAMOUNT = float(row[schema["amount"]])*m  
    # MMex-schema-specific
    if TRANSAMOUNT < 0:
      TRANSCODE = "Withdrawal"
    else:
      TRANSCODE = "Deposit"
  else:
    # There is a column for debits and a column for credits. In this case, we expect both
    # columns to exist and will enforce our own 'signs'
    # First check for debits and then for credits
    TRANSAMOUNT = None
    if "debit_amount" in schema and row[schema["debit_amount"]] != "":
      TRANSAMOUNT = float(row[schema["debit_amount"]])
      TRANSCODE = "Withdrawal"
    elif "credit_amount" in schema and row[schema["credit_amount"]] != "":
      TRANSAMOUNT = float(row[schema["credit_amount"]])
      TRANSCODE = "Deposit"
    if TRANSAMOUNT == "" or TRANSAMOUNT == None :
      raise UserError.UserError("Something is wrong with the way you've defined your amount columns.")
  
  # Transactions are actually stored as absolute values
  TRANSAMOUNT = abs(TRANSAMOUNT)    
    
  # Mark as not yet reconciled  
  STATUS = ""
  
  # Transaction number is an optional field
  if 'transaction_number' in schema and schema['transaction_number'] != "False":
    TRANSACTIONNUMBER = row[schema['transaction_number']]
  else:
    TRANSACTIONNUMBER = None

  if 'notes' in schema:
    NOTES = row[schema['notes']]
  else:
    NOTES = None

  CATEGID = -1
  SUBCATEGID = -1

  # Check if matches any configured categories, and populate schema if so
  cat_id, sub_cat_id = util.get_categoryid_for_payee(PAYEE, categories, db)
  CATEGID = cat_id
  SUBCATEGID = sub_cat_id  

  TRANSDATE = format_date(datetime.datetime.strptime(row[schema['date']], DATE_FORMAT))
  FOLLOWUPID = -1
  TOTRANSAMOUNT = TRANSAMOUNT

 
  t = db.search_transaction(ACCOUNTID=ACCOUNTID, PAYEEID=PAYEEID, TRANSAMOUNT=TRANSAMOUNT, TRANSDATE=TRANSDATE)
  confirm = True
#   print "TRANSID=%s, ACCOUNTID=%s, TOACCOUNTID=%s, PAYEEID=%s, TRANSAMOUNT=%s, TRANSCODE=%s, STATUS=%s, TRANSACTIONNUMBER=%s, NOTES=%s, CATEGID=%s, SUBCATEGID=%s, TRANSDATE=%s, FOLLOWUPID=%s, TOTRANSAMOUNT=%s" % (TRANSID, ACCOUNTID, TOACCOUNTID, PAYEEID, TRANSAMOUNT,  TRANSCODE, STATUS, TRANSACTIONNUMBER, NOTES, CATEGID, SUBCATEGID, TRANSDATE, FOLLOWUPID, TOTRANSAMOUNT)
  if t:
    print "%s - %s : %s (%s)" % (TRANSDATE, PAYEE, TRANSAMOUNT, TRANSCODE)
    confirm = util.query_yes_no("A possible Transaction already exists. Do you want to continue?", default="no")

  if confirm: 
    t = db.save_transaction(TRANSID = TRANSID, ACCOUNTID=ACCOUNTID, TOACCOUNTID=TOACCOUNTID, PAYEEID=PAYEEID, TRANSAMOUNT=TRANSAMOUNT,  TRANSCODE=TRANSCODE, STATUS=STATUS, TRANSACTIONNUMBER=TRANSACTIONNUMBER, NOTES=NOTES, CATEGID=CATEGID, SUBCATEGID=SUBCATEGID, TRANSDATE=TRANSDATE, FOLLOWUPID=FOLLOWUPID, TOTRANSAMOUNT=TOTRANSAMOUNT)
