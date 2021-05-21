
from test import *
from api.toolFunc import *
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
import pandas as pd

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

def get_cases():
    case = pd.read_csv('./api/data/case.csv')
    cdb = CouchDB()
    db = cdb.get_db('australia_location')
    loc = db.get('f03a9af2e5923e35a8bbb528b1590ac4')
    resp = precess_case(case, loc, list(loc.keys()))
    return resp

def get_lang():
    dataset = pd.read_csv('./api/data/language_spoken_at_home.csv')
    f = open('./api/data/vic_geo.json','r')
    vic_loc = json.load(f)
    f.close()
    vic_real_name = []
    for i in vic_loc['features']:
        vic_real_name.append(i['properties']['vic_lga__3'])
    f.close()
    resp = precess_lang(dataset, vic_real_name)

    return resp


def save_area_rent_income_crime():
    crime = pd.read_csv('./api/data/crime.csv').fillna(0)
    income = pd.read_csv('./api/data/income.csv').fillna(0)
    rent = pd.read_csv('./api/data/rent.csv').fillna(0)

    f = open('./api/data/vic_geo.json','r')
    vic = json.load(f)
    f.close()
    loc = []
    for i in vic['features']:
        loc.append(i['properties']['vic_lga__3'])
    resp = {}
    for i in range(len(rent)):
        area = rent.loc[i, ' lga_name16']
        value = rent.loc[i, ' median_sep_2017']
        area_name = wash_lga_name(area,loc)
        if area_name in loc:
            if area_name in resp:
                resp[area_name]['rent'] = int(value)
            else:
                resp[area_name] = {}
                if 'a' not in str(value):
                    resp[area_name]['rent'] = int(value)
                else:
                    resp[area_name]['rent'] = value

    for i in range(len(income)):
        area = income.loc[i, ' lga_name16']
        mean = income.loc[i, ' mean_aud_2014_15']
        median = income.loc[i, 'median_aud_2014_15']
        area_name = wash_lga_name(area, loc)
        if area_name in loc:
            if area_name in resp:
                resp[area_name]['income'] = {}
                resp[area_name]['income']['mean'] = int(mean)
                resp[area_name]['income']['median'] = int(median)
            else:
                resp[area_name] = {}
                resp[area_name]['income'] = {}
                resp[area_name]['income']['mean'] = int(mean)
                resp[area_name]['income']['median'] = int(median)

    crime_name = ['Against the person','Property and deception', 'Drug offences', 'Public order and security', 'Justice procedures', 'Other offences']
    for i in range(len(crime)):
        area = crime.loc[i, 'lga_name11']
        value = crime.loc[i, [' total_division_a_offences',' total_division_b_offences',' total_division_c_offences',' total_division_d_offences',' total_division_e_offences',' total_division_f_offences']]
        area_name = wash_lga_name(area, loc)
        if area_name in loc:
            if area_name in resp:
                resp[area_name]['crime'] = {}
                for c in range(6):
                    resp[area_name]['crime'][crime_name[c]] = int(value[c])
            else:
                resp[area_name] = {}
                resp[area_name]['crime'] = {}
                for c in range(6):
                    resp[area_name]['crime'][crime_name[c]] = int(value[c])

    for k,v in resp.items():
        if 'rent' not in v:
            v['rent'] = None
        if 'income' not in v:
            v['income'] = {'mean':None,'median':None}
        if 'crime' not in v:
            v['crime'] = {}
            for c in range(6):
                v['crime'][crime_name[c]] = None

    cdb = CouchDB()
    ic_db = cdb.create_db('area_rent_income_crime')
    ic_db = cdb.get_db('area_rent_income_crime')
    ic_db.save(resp)
    return resp


import json
from datetime import timedelta
'''
cdb = CouchDB()
a = cdb.create_db('language')
h_db = cdb.get_db('language')
resp = get_lang()
h_db.save(resp)

a = cdb.create_db('cases')
h_db = cdb.get_db('cases')
resp = get_cases()
h_db.save(resp)'''

'''cdb = CouchDB()
e_db = cdb.get_db('melbourne20_21')
a = cdb.create_db('hotword_50_hour')
h_db = cdb.get_db('hotword_50_hour')
table = e_db.iterview('_design/dictionary/_view/textdate',3000)
timeline = get_topN(table)
with open('timeline_all.json','w') as jj:
    json.dump(timeline, jj)

for k,v in timeline.items():
    print(k)
    print(len(list(v.keys())))
    h_db[k] = v'''


resp = save_area_rent_income_crime()
