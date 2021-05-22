# this code is used to listen to the tweets in real time.
import time
import tweepy
from tweepy.streaming import StreamListener
from tweepy import Stream
import json
import re

# get the auth
consumer_key = 'ZcO30H4KGcg69CkuQGG1syyvU'
consumer_secret = '6H8WfyPPrNkcDxwwthtEpT5aJfuozSfmNvl4BwjrSiBD4eJufm'
access_token = '1384360857715449863-3XxwdbavA2s4tUXwUfhZDyVatq55wP'
access_token_secret = 'HNDW798po87e9f2NjqVoSUzW2ecvgcvyUeXFeGAkaXvkT'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#set the keyword and save to th database
def processdata(data):
    dict={}
    dict['id']=data['id_str']
    dict['key']='Australia'
    dict['doc']=data
    db.save(dict)

class LocateListener(StreamListener):

    def __init__(self):
        super().__init__()
        self.limit = 1000
        self.count=0

    def on_data(self, data):
        # limit the speed
        self.count  +=1
        if self.count>=10:
            time.sleep(2)
            self.count=0
        tweetJson = json.loads(data, encoding= 'utf-8')
        # uif the tweet has geo information
        if tweetJson['geo']!=None or tweetJson['coordinates'] or tweetJson['place']:     
            self.counter += 1
            time.sleep(1)
            processdata(tweetJson)
        return True

    def on_error(self, status):
        print (status)

import couchdb
server = couchdb.Server('http://admin:admin@172.26.134.73:5984/')
db = server['has_location_try']
listener = LocateListener()
stream = tweepy.Stream(auth,listener)
stream.filter(locations = [111,-44,155,-9])

