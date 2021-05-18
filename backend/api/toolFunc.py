import json

import jsonlines


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

from collections import Counter

def get_top_word_1(l, data,mode = 'word', n = 20):
    total = Counter({})
    for i in data.view('_all_docs'):
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
    resp = {'series':[]}
    c = 0
    if mode == 'word':
        for k, v in total.items():
            resp['series'].append(make_name_data(k,v))
            if c >= n:
                return resp
            c += 1
    else:
        hash_total = get_all_hashtags(total)
        for k, v in hash_total.items():
            resp['series'].append(make_name_data(k,v))
            if c >= n:
                return resp
            c += 1
    return resp

def generate_data_key(start, end):
    l = []
    delta = timedelta(hours=1)
    start = get_time(start)
    end =  get_time(end)
    while start < end:
        l.append(start.strftime('%Y/%m/%d/%H'))
        start += delta
    return l