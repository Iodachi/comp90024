# this code is used to search for the twitters from the past week in a setted circle.
import tweepy
import json
import requests

# THE locations which are very near to each other so the  radius is set to 8km
locs_small=['KNOX',
 'MAROONDAH',
 'HOBSONS BAY',
 'MELBOURNE',
 'MANNINGHAM',
 'GREATER DANDENONG',
 'WHITEHORSE',
 'MOONEE VALLEY',
 'PORT PHILLIP',
 'BAYSIDE',
 'BRIMBANK',
 'FRANKSTON',
 'STONNINGTON',
 'KINGSTON',
 'BOROONDARA',
 'MORELAND',
 'GLEN EIRA',
 'BANYULE',
 'MONASH',
 'MARIBYRNONG',
 'DAREBIN']
# THE locations which are further to each other so the  radius is set to 14km
locs_mid=['MELTON',
 'WYNDHAM',
 'WHITTLESEA',
 'HUME',
 'YARRA RANGES',
 'CASEY',
 'NILLUMBIK']
# THE locations which are very far away to each other so the  radius is set to 80km
locs_large=['GREATER BENDIGO', 'YARRIAMBIACK', 'ALPINE', 'LATROBE', 'SOUTHERN GRAMPIANS'] 
dis =['8km','14km','80km']

# get author from tweet.api
consumer_key = 'ZcO30H4KGcg69CkuQGG1syyvU'
consumer_secret = '6H8WfyPPrNkcDxwwthtEpT5aJfuozSfmNvl4BwjrSiBD4eJufm'
access_token = '1384360857715449863-3XxwdbavA2s4tUXwUfhZDyVatq55wP'
access_token_secret = 'HNDW798po87e9f2NjqVoSUzW2ecvgcvyUeXFeGAkaXvkT'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
until = '2021-05-23'

# set the database to use
import couchdb
server = couchdb.Server('http://admin:admin@172.26.134.73:5984/')
db = server['has_location_in_vic']

for loc in locs_small:
    # get the lat and lng from google api
    request = ('https://maps.googleapis.com/maps/api/geocode/json?address='
                     + loc+',VIC' +',AU'+ '&key=AIzaSyDLyQLWVoJpRYadYLuIffczAYjmr3CCvo0')
    response = requests.get(request)
    response.raise_for_status()
    lat = json.loads(response.text)['results'][0]['geometry']['location']['lat']
    lng = json.loads(response.text)['results'][0]['geometry']['location']['lng']
    geocode = str(round(lat,3))+','+str(round(lng,3))+','+dis[0]
    print(geocode)
    tweets = api.search(q='*',geocode =geocode,count=100,until = until)
    count=0
    for tweet in tweets:
        count = count+1
        json_str = json.dumps(tweet._json)
        ans={}
        ans['id'] = tweet._json['id_str']
        ans['key'] = ''+ loc
        ans['geo'] = [lat,lng]
        ans['doc'] = tweet._json
        db.save(ans)
    print(count,loc)

for loc in locs_mid:
    request = ('https://maps.googleapis.com/maps/api/geocode/json?address='
                     + loc+',VIC' +',AU'+ '&key=AIzaSyDLyQLWVoJpRYadYLuIffczAYjmr3CCvo0')
    response = requests.get(request)
    response.raise_for_status()
    lat = json.loads(response.text)['results'][0]['geometry']['location']['lat']
    lng = json.loads(response.text)['results'][0]['geometry']['location']['lng']
    geocode = str(round(lat,3))+','+str(round(lng,3))+','+dis[1]
    print(geocode)
    tweets = api.search(q='*',geocode =geocode,count=100,until = until)
    count=0
    for tweet in tweets:
        count = count+1
        json_str = json.dumps(tweet._json)
        ans={}
        ans['id'] = tweet._json['id_str']
        ans['key'] = ''+ loc
        ans['geo'] = [lat,lng]
        ans['doc'] = tweet._json
        db.save(ans)
    print(count,loc)

for loc in locs_large:
    request = ('https://maps.googleapis.com/maps/api/geocode/json?address='
                     + loc+',VIC' +',AU'+ '&key=AIzaSyDLyQLWVoJpRYadYLuIffczAYjmr3CCvo0')
    response = requests.get(request)
    response.raise_for_status()
    lat = json.loads(response.text)['results'][0]['geometry']['location']['lat']
    lng = json.loads(response.text)['results'][0]['geometry']['location']['lng']
    geocode = str(round(lat,3))+','+str(round(lng,3))+','+dis[2]
    print(geocode)
    tweets = api.search(q='*',geocode =geocode,count=100,until = until)
    count=0
    for tweet in tweets:
        count = count+1
        json_str = json.dumps(tweet._json)
        ans={}
        ans['id'] = tweet._json['id_str']
        ans['key'] = ''+ loc

        ans['geo'] = [lat,lng]
        ans['doc'] = tweet._json
        db.save(ans)
    print(count,loc)
