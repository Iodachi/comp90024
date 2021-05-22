from backend.api.toolFunc import get_time
import json
from backend.test import *

cdb = CouchDB()

db = cdb.get_db('sentiment_covid')