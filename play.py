import json
from backend.test import *


json_file = {'series':[]}
with open('./backend/api/data/Employment - Accommodation and Food Services.json') as f:
    temp = json.load(f)
    num15, num19, num20 = 0,0,0
    data = {}
    for i in temp['features']:
        num15+=int(i['properties']['nov_15'])
        num19+=int(i['properties']['nov_19'])
        num20+=int(i['properties']['nov_20'])
        data['name'] = i['properties']['ind']
    data['data'] = [num15,num19,num20]

    json_file['series'].append(data)

with open('./backend/api/data/Employment - Education and Training.json') as f:
    temp = json.load(f)
    num15, num19, num20 = 0,0,0
    data = {}
    for i in temp['features']:
        num15+=int(i['properties']['nov_15'])
        num19+=int(i['properties']['nov_19'])
        num20+=int(i['properties']['nov_20'])
        data['name'] = i['properties']['ind']
    data['data'] = [num15,num19,num20]

    json_file['series'].append(data)

with open('./backend/api/data/Employment - Health Care and Social Assistance.json') as f:
    temp = json.load(f)
    num15, num19, num20 = 0,0,0
    data = {}
    for i in temp['features']:
        num15+=int(i['properties']['nov_15'])
        num19+=int(i['properties']['nov_19'])
        num20+=int(i['properties']['nov_20'])
        data['name'] = i['properties']['ind']
    data['data'] = [num15,num19,num20]

    json_file['series'].append(data)

with open('./backend/api/data/Employment - Rental, Hiring and Real Estate.json') as f:
    temp = json.load(f)
    num15, num19, num20 = 0,0,0
    data = {}
    for i in temp['features']:
        num15+=int(i['properties']['nov_15'])
        num19+=int(i['properties']['nov_19'])
        num20+=int(i['properties']['nov_20'])
        data['name'] = i['properties']['ind']
    data['data'] = [num15,num19,num20]

    json_file['series'].append(data)



