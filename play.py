from backend.api.toolFunc import get_time
import json
from backend.test import *

cdb = CouchDB()
#test = cdb.create_db('ccc')
all_db = cdb.get_db('melbourne2016')
table_all = all_db.view('_design/dictionary/_view/language', key = 'en')

for i in table_all:
    print(i)

