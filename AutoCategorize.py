from mmeximporter import MMexDB, Settings, UserError
import util
import sys, os
import csv
import datetime
from models import Transaction, CategoryID, SubCategoryID

confirm = util.query_yes_no("This will recategorize all transactions, are you sure?")
if not confirm:
  sys.exit(-1)
  
settings = Settings.Settings()
categories = settings.getCategories()
db = MMexDB.MMexDb(settings)

accounts = db.get_all_accounts()

for account in accounts:
  print "Updating account: %s" % (account.ACCOUNTNAME)
  transactions = db.get_transactions(account.ACCOUNTNUM)
  for t in transactions:
    payee_name = db.get_payee_name(t.PAYEEID)
    cat_id, sub_cat_id = util.get_categoryid_for_payee(payee_name, categories, db)
    t.CATEGID = cat_id
    t.SUBCATEGID = sub_cat_id
    t.save()