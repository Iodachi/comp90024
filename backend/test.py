import couchdb

DB_INFO= {
    'username': 'admin',
    'password': 'admin',
    'host': '172.26.133.210',
    'port': '5984',
}



class CouchDB(object):
    db = {}
    connected = False
    url = ''
    server = None

    def __init__(self, db_info = DB_INFO):
        self.url = 'http://' + db_info['username'] + ':' + db_info['password'] + '@' + db_info['host'] + ':' + db_info['port'] + '/'

        try:
            self.server = couchdb.Server(self.url)
            self.connected = True
            print('Success connected CouchDB Server with url:{', self.url, '}')
        except Exception:
            self.server = None
            self.connected = False
            print('Connection FAILED to CouchDB Server with url:{', self.url, '}')

    def get_db(self, db_name):
        if self.connected:
            if db_name in self.server:
                print('Success return database of %s' % db_name)
                return self.server[db_name]
            else:
                print('In get_db(): Database name [%s] does not exist!' % db_name)
                return None
        else:
            print('In get_db(): Server is not connected')
            return None
    
    def create_db(self, db_name):
        if self.connected:
            if db_name in self.server:
                print('In create_db(): Database [%s] already exist' % db_name)
                return None
            else:
                db = self.server.create(db_name)
                print('Database [%s] created' % db_name)
                return db
        else:
            print('In create_db(): Server is not connected')
            return None
'''import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
#nltk.download('stopwords')
cdb = CouchDB()
twitter_db = cdb.get_db('melbourne_2020')
print('here')
view =  twitter_db.iterview('_design/new views/_view/create-at_text',100)
c = 0
for v in view:
    c+=1
    print(v.key[0], v.key[1])
print(c)'''