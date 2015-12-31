'''
@author: ssuppe
'''

from UserError import UserError
import os
import json

class Settings:

    config = json.loads(open('mmeximporter.cfg', 'r').read())

    def __init__(self):
        if not os.path.isfile(self.config['dbfile']):
            raise UserError("Cannot find configuration file: ", self.config['dbfile'])    

    @property
    def mmex_dbfile(self):
        result = self.config['dbfile']
        if not result or result == '':
            raise UserError("Location to the MMex DB file is missing in the config.")
        return result
        
    def __str__(self):
      return "DB File: " + self.config['dbfile']

    def __repr__(self):
      return self.__str__()
      
    def getSchema(self, account_number):
      try:
        return self.config['schemas'][account_number]
      except:
        raise UserError("Account %s is missing from 'schemas' in mmeximporter.cfg" % (account_number))

    def getCategories(self):
      try:
        return self.config['categories']
      except:
        raise UserError("Categories missing from config files, or malformed.")