from backend.api.toolFunc import get_time
import json
from backend.test import *

cdb = CouchDB()
db = cdb.get_db('melbourne20_21')
table = db.view('_design/dictionary/_view/date', group=True, group_level=1)

for v in table:
    print(v.key, v.value)

