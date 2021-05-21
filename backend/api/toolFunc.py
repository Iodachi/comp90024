import json
from tqdm import tqdm
import jsonlines
import random

def read_small_json(input_file):
    with open(input_file) as f:
        data = json.load(f)
    return data

def read_json_line(input_file, n):
    data = {}
    c = 0
    with jsonlines.open(input_file) as reader:
        for obj in reader:
            if c < n:
                data[c] = obj
                c += 1
            else:
                break
    return data

def read_n_line(n, mode):
    try:
        if int(n) <= 0:
            print('ERROR: Number of line requested must greater than 0!!!')
            return None
        # Opening JSON file
        n = int(n)
        if mode == 'raw':
            data = read_json_line('./backend/api/data/test.data.jsonl', n)
        
        return data
    except:
        print('ERROR: Number of line requested is illegal!!!')
        return None

def get_all_hashtags(data):
    hashtags = {}
    for word, frequency in data.items():
        if word.startswith("#") and len(word) > 1:
            hashtags[word] = frequency
    return dict(sorted(hashtags.items(), key=lambda item: item[1],reverse=True))

def make_name_data(name, data):
    resp = {}
    resp['name'] = name
    resp['data'] = data
    return resp

from datetime import datetime, timedelta

def get_time(elm):
    if len(elm) > 14:
        date = datetime.strptime(elm, '%a-%b-%d-%H:%M:%S-+0000-%Y')
    else:
        date = datetime.strptime(elm, '%Y/%m/%d/%H')
    return date

def get_front_time(time_str):
    data = datetime.strptime(time_str, '%b-%d-%Y-%H:%M:%S')
    return data

from collections import Counter

def get_top_word_1(l, data,mode = 'word', n = 20):
    total = Counter({})
    for i in tqdm(data.view('_all_docs')):
        if i.id in l:
            w = data.get(i.id)
            w.pop('_id')
            w.pop('_rev')
            total += Counter(w)

    print('finish')
    total = dict(total)
    if 'rt' in total:
        total.pop('rt')
    total = dict(sorted(total.items(), key=lambda item: item[1],reverse=True))
    resp = {'series':[{'data':[]}], 'name':[]}
    c = 1
    if mode == 'word':
        for k, v in total.items():
            resp['series'][0]['data'].append(v)
            resp['name'].append(k)
            if c >= n:
                return resp
            c += 1
    else:
        hash_total = get_all_hashtags(total)
        for k, v in hash_total.items():
            resp['series'][0]['data'].append(v)
            resp['name'].append(k)
            if c > n:
                return resp
            c += 1
    return resp

def generate_data_key(start, end):
    l = []
    delta = timedelta(hours=1)
    start = get_front_time(start)
    end =  get_front_time(end)
    while start < end:
        l.append(start.strftime('%Y/%m/%d/%H'))
        start += delta
    return l


def wash_lga_name(lga_name, real_name):
    dif_len, a_len, b_len = 0,0,0
    lga_name = lga_name.replace('-',' ')
    result_name = '_'
    for name in real_name:
        if name.lower() in lga_name.lower():
            if a_len == 0:
                a_len = len(name)
                b_len = len(lga_name)
                dif_len = abs(a_len - b_len)
                result_name = name
            else:
                a_len = len(name)
                b_len = len(lga_name)
                if abs(a_len-b_len) < dif_len:
                    dif_len = abs(a_len - b_len)
                    result_name = name
    if len(result_name) == 0:
        return lga_name
    else:
        return result_name


def precess_lang(dataset,rname):
    resp = {}

    for index in tqdm(range(len(dataset))):
        area = dataset.loc[index, 'LGA 2011']
        real_name = wash_lga_name(area, rname)
        if real_name in rname:
            if real_name in resp:
                lang_name = dataset.loc[index, 'Language Spoken at Home'].replace('\"','')
                if 'total' in lang_name.lower() or 'other' in lang_name.lower():
                    continue
                if lang_name in resp[real_name]:
                    resp[real_name][lang_name] += int(dataset.loc[index, 'Value'])
                else:
                    resp[real_name][lang_name] = int(dataset.loc[index, 'Value'])
            else:
                resp[real_name] = {}
                lang_name = dataset.loc[index, 'Language Spoken at Home'].replace('\"','')
                if 'total' in lang_name or 'other' in lang_name:
                    continue
                resp[real_name][lang_name] = int(dataset.loc[index, 'Value'])

    return resp
        


def make_geo(loc):
    a = loc.copy()
    a.reverse()
    di = {"type":"Feature","properties":{},"geometry": { "type": "Point"} }
    di["geometry"]["coordinates"] = a
    return di


def precess_case(dataset, loc, rname):
    resp = {"type": "FeatureCollection","features": []}
    for index in range(len(dataset)):
        lga_name = dataset.loc[index, 'Localgovernmentarea']
        real_name = wash_lga_name(lga_name, rname)
        if real_name in loc:
            cord = loc[real_name]
        else:
            cord = loc['Melbourne']
        geo = make_geo(cord)
        resp['features'].append(geo)
    return resp


def random_float(low, high):
    return random.random()*(high-low) + low

def precess_au_heatmap(view):
    resp = {"type": "FeatureCollection","features": []}
    for v in view:
        if v[0]:
            cord = v[0].copy().reverse()
        if v[1]:
            cord = v[0].copy().reverse()
        if v[2]:
            if len(v[2][0]) == 4:
                x = random_float(v[2][0][0][0], v[2][2][0][0])
                y = random_float(v[2][0][0][1], v[2][2][0][1])
                cord = [x,y]
        geo = make_geo(cord)
        resp['features'].append(geo)
    return resp

def process_lang_heatmap(view):
    resp = {"type": "FeatureCollection","features": []}
    for v in view:
        cord = v.value.copy()
        cord.reverse()
        geo = make_geo(cord)
        resp['features'].append(geo)
    return resp

