'''

@author: suppe
'''

import sqlite3
import logging
import UserError
from models import Account, Transaction, Payee, db
import peewee

class MMexDb:
    '''
    Implements the interactions with MMex Database
    '''

    __logger = logging.getLogger('MMexDB')
    
    __conn = None
    
    def __init__(self, settings):
        db.init(settings.mmex_dbfile)
                    
    def save_transaction(self, TRANSID, ACCOUNTID, TOACCOUNTID, PAYEEID, TRANSAMOUNT,  TRANSCODE, STATUS, TRANSACTIONNUMBER, NOTES, CATEGID, SUBCATEGID, TRANSDATE, FOLLOWUPID, TOTRANSAMOUNT):
      t = Transaction.create(TRANSID = TRANSID, ACCOUNTID=ACCOUNTID, TOACCOUNTID=TOACCOUNTID, PAYEEID=PAYEEID, TRANSAMOUNT=TRANSAMOUNT,  TRANSCODE=TRANSCODE, STATUS=STATUS, TRANSACTIONNUMBER=TRANSACTIONNUMBER, NOTES=NOTES, CATEGID=CATEGID, SUBCATEGID=SUBCATEGID, TRANSDATE=TRANSDATE, FOLLOWUPID=FOLLOWUPID, TOTRANSAMOUNT=TOTRANSAMOUNT)
      id = t.TRANSID
      return id
    
    def search_transaction(self, ACCOUNTID, PAYEEID, TRANSAMOUNT, TRANSDATE):
      try:
        t = Transaction.select().where((Transaction.ACCOUNTID==ACCOUNTID) & (Transaction.PAYEEID==PAYEEID) & (Transaction.TRANSAMOUNT==TRANSAMOUNT) & (Transaction.TRANSDATE==TRANSDATE)).get()
        return True
      except peewee.DoesNotExist:
        return False
    
    def get_transactions(self, account_number):
      db_account_id = self.get_accountid(account_number)
      trans = Transaction.select().where(Transaction.ACCOUNTID==db_account_id)
#       print "Num trans:", len(trans)
      results = []
      for row in trans:
        results.append(row)
      return results
    
    def get_accountid(self, account_number):
        accts = Account.select().where(Account.ACCOUNTNUM == account_number)
        if (len(accts) > 1):
            raise UserError("There are multiple accounts in MoneyManagerEx with the same number:", account_number)
        return accts.get().ACCOUNTID
        
    def get_payeeid(self, payee_str):
        try:
          id = Payee.select().where(Payee.PAYEENAME == payee_str.strip()).get()
          return id.PAYEEID
        except peewee.DoesNotExist as e:
          return None
    
    def register_payeeid(self, payee_str):
        id = self.get_payeeid(payee_str)
        if id == None:
          payee = Payee.create(PAYEENAME=payee_str.strip(), CATEGID=-1, SUBCATEGID=-1)
          id = self.get_payeeid(payee_str)
        return id
    