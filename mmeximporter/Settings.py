'''
@author: ssuppe
'''

import UserError
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
      return self.config['schemas'][account_number]
#     
#     @property
#     def categories(self):
#         result = []
#         cat_sections = (sec for sec in self.config.sections() if sec.startswith('category-'))
#         for sec in cat_sections:
#             categories = sec[9:].split(':', 2)
#             categories.append(None)
#             status = self.config[sec]['status']
#             conditions = []
#             counter = 1
#             while 'field'+str(counter) in self.config[sec]:
#                 conditions.append((self.config[sec]['field'+str(counter)],
#                                    self.config[sec]['operator'+str(counter)],
#                                    self.config[sec]['value'+str(counter)]))
#                 counter = counter + 1
#             result.append({'category':categories[0], 'subcategory':categories[1],
#                            'status':status, 'conditions':conditions})
#         return result