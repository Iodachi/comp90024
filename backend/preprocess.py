
from test import *
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
def make_name_data(name, data):
    resp = {}
    resp['name'] = name
    resp['data'] = data
    return resp

def get_word_freq(d, ll):
    sentence_temp = d.copy()
    reg = re.compile(r'[a-z]')
    stopword = set(stopwords.words('english'))
    for word in ll:
        word = word.replace('_', '')
        flag = 0
        #remove stopwords
        if word in stopword:
            flag = 1
            continue
        #remove any word that does not contain any English alphabets
        if not reg.match(word):
            flag = 1
            for c in word:
                if ord(c) >= 97 and ord(c) <= 122: 
                    flag = 0
                    break
        if not flag:
            if word in sentence_temp: sentence_temp[word]+=1
            else: sentence_temp[word] = 1
    
    sentence_temp = dict(sorted(sentence_temp.items(), key=lambda item: item[1],reverse=True))
    new ={}
    c = 0
    for k, v in sentence_temp.items():
        new[k] = v
        c+=1
        if c > 51:
            break
    return new

def get_all_hashtags(data):
    hashtags = {}
    for word, frequency in data.items():
        if word.startswith("#") and len(word) > 1:
            hashtags[word] = frequency
    return dict(sorted(hashtags.items(), key=lambda item: item[1],reverse=True))

from datetime import datetime
def get_time(elm):
    date = datetime.strptime(elm, '%a-%b-%d-%H:%M:%S-+0000-%Y')
    return date

from tqdm import tqdm
def get_topN(table):
    
    tt = TweetTokenizer()
    delta = timedelta(hours=1)
    
    timeline = {}

    for tweet in tqdm(table):
        text = tweet.key[1]
        time_str = tweet.key[0].replace(' ','-')
        time = get_time(time_str)
        timeb = datetime(2020,1,1,0,0,0,0)
        while timeb < datetime.now():
            timeS = timeb
            timeE = timeb + delta
            if time > timeS and time < timeE:
                if timeS.strftime('%Y/%m/%d/%H') in timeline:
                    word_freq = timeline[timeS.strftime('%Y/%m/%d/%H')].copy()
                    ll = [w.lower() for w in tt.tokenize(text)]
                    word_freq = get_word_freq(word_freq,ll)
                    timeline[timeS.strftime('%Y/%m/%d/%H')] = word_freq.copy()

                else:
                    word_freq ={}
                    ll = [w.lower() for w in tt.tokenize(text)]
                    word_freq = get_word_freq(word_freq,ll)
                    timeline[timeS.strftime('%Y/%m/%d/%H')] = word_freq.copy()
            timeb += delta
        #print(timeline.keys())

    return timeline


import json
from datetime import timedelta
cdb = CouchDB()
e_db = cdb.get_db('melbourne2020_all')
a = cdb.create_db('hotword_50')
h_db = cdb.get_db('hotword_50')
table = e_db.iterview('_design/dictionary/_view/text_data',3000)
timeline = get_topN(table)
with open('timeline.json','w') as jj:
    json.dump(timeline, jj)

for k,v in timeline.items():
    print(k)
    print(len(list(v.keys())))
    h_db[k] = v

'''{
            "name": "Python: Django",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/backend/manage.py",
            "args": [
                "runserver"
            ],
            "django": true
        }'''
