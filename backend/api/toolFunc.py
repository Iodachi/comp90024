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
    

def make_name_data(name, data):
    resp = {}
    resp['name'] = name
    resp['data'] = data
    return resp