from peewee import Model, IntegerField, CharField, FloatField, SqliteDatabase

db = SqliteDatabase(None)

class Transaction(Model):
  
  TRANSID = IntegerField(db_column="TRANSID",primary_key=True)
  ACCOUNTID = IntegerField(db_column="ACCOUNTID", null=False)
  TOACCOUNTID = IntegerField(db_column="TOACCOUNTID")
  PAYEEID = IntegerField(db_column="PAYEEID", null=False)
  TRANSCODE = CharField(db_column="TRANSCODE")
  TRANSAMOUNT = FloatField(db_column="TRANSAMOUNT", null=False)
  STATUS = CharField(db_column="STATUS")
  TRANSACTIONNUMBER = CharField(db_column="TRANSACTIONNUMBER")
  NOTES = CharField(db_column="NOTES")
  CATEGID = IntegerField(db_column="CATEGID")
  SUBCATEGID = IntegerField(db_column="SUBCATEGID")
  TRANSDATE = CharField(db_column="TRANSDATE")
  FOLLOWUPID = IntegerField(db_column="FOLLOWUPID")
  TOTRANSAMOUNT = FloatField(db_column="TOTRANSAMOUNT")
  
  def __str__(self):
    return "<Transaction: Account DBID: %s, Date: %s,  PayeeID: %s, Amount: %s>" %(str(self.ACCOUNTID), str(self.TRANSDATE), str(self.PAYEEID), str(self.TRANSAMOUNT))
    
  def __repr__(self):
    return self.__str__()
  
  class Meta:
    database = db
    db_table = "CHECKINGACCOUNT_V1"
  


class Account(Model):
    # NOTE: Incomplete list of fields (used for read-only)
    ACCOUNTID = IntegerField(db_column="ACCOUNTID", primary_key=True)
    ACCOUNTNAME = CharField(db_column="ACCOUNTNAME")
    ACCOUNTNUM = IntegerField(db_column="ACCOUNTNUM")
    
    class Meta:
      database = db
      db_table = "ACCOUNTLIST_V1"
      
    def __str__(self):
      return "<Account: Account ID: %s, Name: %s, Number: %s>" %(str(self.ACCOUNTID), str(self.ACCOUNTNAME), str(self.ACCOUNTNUM))
    
    def __repr__(self):
      return self.__str__()

      
class Payee(Model):
    PAYEEID = IntegerField(db_column="PAYEEID", primary_key=True)
    PAYEENAME = CharField(db_column="PAYEENAME", null=False)
    CATEGID = IntegerField(db_column="CATEGID")
    SUBCATEGID = IntegerField(db_column="SUBCATEGID")
    
    class Meta:
      database = db
      db_table = "PAYEE_V1"
      
    def __str__(self):
      return "<Payee: %s, %s>" % (self.PAYEEID, self.PAYEENAME)
      
class CategoryID(Model):
  CATEGID = IntegerField(db_column="CATEGID", primary_key=True)
  CATEGNAME = CharField(db_column="CATEGNAME", null=False, unique=True)
  
  class Meta:
    database = db
    db_table = "CATEGORY_V1"
    
  def __str__(self):
    return "<Category: %s, %s>" % (self.CATEGID, self.CATEGNAME)

class SubCategoryID(Model):
  SUBCATEGID = IntegerField(db_column="SUBCATEGID", primary_key=True)
  SUBCATEGNAME = CharField(db_column="SUBCATEGNAME", null=False)
  CATEGID = IntegerField(db_column="CATEGID")
  
  class Meta:
    database = db
    db_table = "SUBCATEGORY_V1"
    
  def __str__(self):
    return "<SubCategory: %s, %s, %s>" % (self.SUBCATEGID, self.CATEGNAME, self.CATEGID)
    
  