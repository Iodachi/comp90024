
from test import *
from api.toolFunc import *
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
import pandas as pd
import json
from datetime import timedelta

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

'''def conver_hour_day():
    cdb = CouchDB()
    h_db = cdb.get_db('hotword_50_hour')
    key_str = ''
    for i in tqdm(data.view('_all_docs')):
        if key_str != i.id[:-2]
        if i.id in l:
            w = data.get(i.id)
            w.pop('_id')
            w.pop('_rev')
            total += Counter(w)'''

def save_au_heat():
    cdb = CouchDB()
    au_db = cdb.get_db('has_location_try')
    table = au_db.iterview('_design/dictionary/_view/geo',3000)
    resp = {}
    resp = precess_au_heatmap(table)
    ic_db = cdb.create_db('au_heatmap')
    ic_db = cdb.get_db('au_heatmap')
    ic_db.save(resp)
    return resp



def save_area_age():
    age = pd.read_csv('./api/data/age.csv')
    f = open('./api/data/vic_geo.json','r')
    vic = json.load(f)
    f.close()

    loc = []
    for i in vic['features']:
        loc.append(i['properties']['vic_lga__3'])

    aa = []
    for i in range(86):
        if i % 5 == 0:
            aa.append('%d - %d' % (i, i+4)) 
    resp = {}
    for i in range(len(age)):
        area = age.loc[i, ' lga_name']
        pop = age.loc[i, [        ' _0_4_yrs_proj_count',   ' _5_9_yrs_proj_count', 
                                ' _10_14_yrs_proj_count', ' _15_19_yrs_proj_count', 
                                ' _20_24_yrs_proj_count', ' _25_29_yrs_proj_count',
                                ' _30_34_yrs_proj_count', ' _35_39_yrs_proj_count',
                                ' _40_44_yrs_proj_count', ' _45_49_yrs_proj_count',
                                ' _50_54_yrs_proj_count', ' _55_59_yrs_proj_count',
                                ' _60_64_yrs_proj_count', ' _65_69_yrs_proj_count',
                                ' _70_74_yrs_proj_count', '_75_79_yrs_proj_count',
                                ' _80_84_yrs_proj_count',' _85_yrs_over_proj_count']]
        
        area_name = wash_lga_name(area,loc)

        if area_name in loc:
            resp[area_name] = {}
            resp[area_name]['data'] = {}
            ge = []
            for i in pop:
                ge.append(int(i))
            resp[area_name]['data']['count'] = ge
            resp[area_name]['data']['labels'] = aa


    cdb = CouchDB()
    ric_db = cdb.create_db('area_age')
    ric_db = cdb.get_db('area_age')

    ric_db['age'] = resp
    return resp


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


#resp = save_area_age()



def save_lang_heat():
    cdb = CouchDB()
    au_db = cdb.get_db('melbourne2016')
    rtable = au_db.view('_design/dictionary/_view/reducelanguage',group = True)
    big_resp = {}
    for lang in rtable:
        table = au_db.view('_design/dictionary/_view/language', key = lang.key)
        resp = process_lang_heatmap(table)
        big_resp[lang.key] = resp
    s_db = cdb.create_db('heatmap_lang')
    s_db = cdb.get_db('heatmap_lang')
    for k,v in big_resp.items():
        print(k)
        s_db[k] = v
    return big_resp

