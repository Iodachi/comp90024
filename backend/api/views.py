from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest
import ujson
import json
from api.toolFunc import *
import couchdb
from test import *
import pandas as pd

# Create your views here.
print('http://127.0.0.1:8000/api/test/3')
def get_n_tweet(request, n):
    if request.method == 'GET':
        resp = read_n_line(n, 'raw')
        if resp:
            return HttpResponse(ujson.dumps(resp), content_type='application/json')
        else:
            return HttpResponseBadRequest(resp)
    else:
        return HttpResponseBadRequest('request should be get')


print('http://127.0.0.1:8000/api/death/all')
def get_death_number(request, month):
    if request.method == 'GET':
        resp = {'series': []}
        try:
            cdb = CouchDB()
            death_db = cdb.get_db('death')
            if death_db:
                data = death_db['20f65008d43b65f035c3fc6f4a2399c6']
                d = {}
                if month == 'all':
                    for k, v in data.items():
                        if k != 'category' and k[0] != '_':
                            d['name'] = k
                            d['data'] = v
                            resp['series'].append(d)
                            d = {}

                elif month in data['category']:
                    m = data['category'].index(month)
                    for k, v in data.items():
                        if k != 'category' and k[0] != '_':
                            d['name'] = k
                            d['data'] = v[m]
                            resp['series'].append(d)
                            d = {}
                else:
                    resp = None
        
        except Exception:
            resp = None

        if resp:
            print(ujson.dumps(resp))
            return HttpResponse(json.dumps(resp), content_type='application/json')
        else:
            return HttpResponseBadRequest(resp)
    else:
        return HttpResponseBadRequest('request should be GET')




print('http://127.0.0.1:8000/api/employment')
def get_employment(request):
    if request.method == 'GET':
        cdb = CouchDB()
        e_db = cdb.get_db('employment')
        data = e_db['20f65008d43b65f035c3fc6f4a23ccec']
        resp = data
        if resp:
            return HttpResponse(ujson.dumps(resp), content_type='application/json')
        else:
            return HttpResponseBadRequest(resp)
    else:
        return HttpResponseBadRequest('request should be get')

print('http://127.0.0.1:8000/api/tweet/top/word/20/Oct-12-2020-00:00:00/Oct-13-2020-00:00:00')
def get_top(request, mode = 'word', n = 20, timeS = None, timeE=None):
    if request.method == 'GET':
        cdb = CouchDB()
        data = cdb.get_db('hotword_50_hour')
        l = generate_data_key(timeS,timeE)
        print('here')
        resp = get_top_word_1(l,data, mode, n)
        if resp:
            return HttpResponse(ujson.dumps(resp), content_type='application/json')
        else:
            return HttpResponseBadRequest(resp)
    else:
        return HttpResponseBadRequest('request should be get')


print('http://127.0.0.1:8000/api/cases')
def get_cases(request):
    if request.method == 'GET':
        cdb = CouchDB()
        db = cdb.get_db('cases')
        resp = db.get('dc03849c597d859fe1dbe170262687d0')
        resp.pop('_id')
        resp.pop('_rev')
        with open('geo.json','w') as ff:
            json.dump(resp, ff)
        if resp:
            return HttpResponse(ujson.dumps(resp), content_type='application/json')
        else:
            return HttpResponseBadRequest(resp)
    else:
        return HttpResponseBadRequest('request should be get')


print('http://127.0.0.1:8000/api/language')
def get_lang(request):
    if request.method == 'GET':
        cdb = CouchDB()
        db = cdb.get_db('language')
        resp = db.get('7c78cc675e58cf2a48b4bd9093e153ff')
        resp.pop('_id')
        resp.pop('_rev')

        if resp:
            return HttpResponse(json.dumps(resp), content_type='application/json')
        else:
            return HttpResponseBadRequest(resp)
    else:
        return HttpResponseBadRequest('request should be get')


print('http://127.0.0.1:8000/api/area/info')
def get_areaInfo(request):
    if request.method == 'GET':
        cdb = CouchDB()
        db = cdb.get_db('area_rent_income_crime')
        resp = db.get('bdb85cf015fe7fe55ca28dd28cd3f2f4')
        resp.pop('_id')
        resp.pop('_rev')

        if resp:
            return HttpResponse(json.dumps(resp), content_type='application/json')
        else:
            return HttpResponseBadRequest(resp)
    else:
        return HttpResponseBadRequest('request should be get')

print('http://127.0.0.1:8000/api/area/age')
def get_areaAge(request):
    if request.method == 'GET':
        cdb = CouchDB()
        db = cdb.get_db('area_age')
        resp = db.get('age_15')
        resp.pop('_id')
        resp.pop('_rev')

        if resp:
            return HttpResponse(json.dumps(resp), content_type='application/json')
        else:
            return HttpResponseBadRequest(resp)
    else:
        return HttpResponseBadRequest('request should be get')

print('http://127.0.0.1:8000/api/language/heatmap/en')
def get_langHeat(request, lang):
    if request.method == 'GET':
        cdb = CouchDB()
        db = cdb.get_db('heatmap_lang')
        if lang not in db:
            return HttpResponseBadRequest('language not exist')
        resp = db.get(lang)
        resp.pop('_id')
        resp.pop('_rev')

        if resp:
            return HttpResponse(json.dumps(resp), content_type='application/json')
        else:
            return HttpResponseBadRequest(resp)
    else:
        return HttpResponseBadRequest('request should be get')