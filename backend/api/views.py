from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest
import ujson
import json
from api.toolFunc import *
import couchdb
from test import *

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