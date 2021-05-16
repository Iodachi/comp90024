from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest
import ujson
import json
from api.toolFunc import *
import couchdb
from test import *

# Create your views here.
print('http://127.0.0.1:8000/api/3')
def get_n_tweet(request, n):
    if request.method == 'GET':
        resp = read_n_line(n, 'raw')
        if resp:
            return HttpResponse(ujson.dumps(resp), content_type='application/json')
        else:
            return HttpResponseBadRequest(resp)
    else:
        return HttpResponseBadRequest('request should be get')

def get_death_number(request, month):
    if request.method == 'GET':
        resp = {}
        try:
            cdb = CouchDB()
            death_db = cdb.get_db('death')
            if death_db:
                data = death_db['20f65008d43b65f035c3fc6f4a2399c6']
                if month == 'all':
                    for k, v in data.items():
                        if k != 'category':
                            resp[k] = v
                elif month in data['category']:
                    m = data['category'].index(month)
                    for k, v in data.items():
                        if k != 'category':
                            resp[k] = v[m]
                else:
                    resp = None
        
        except Exception:
            resp = None

        if resp:
            return HttpResponse(ujson.dumps(resp), content_type='application/json')
        else:
            return HttpResponseBadRequest(resp)
    else:
        return HttpResponseBadRequest('request should be GET')