# this code is used to listen to the tweets in real time.
import time
import tweepy
from tweepy.streaming import StreamListener
from tweepy import Stream
import json
import re

# get the auth
consumer_key = 'ttxVysxszrgEJcKPwqSEIii5r'
consumer_secret = 'nGGY750XCBrAuXxYJ1zWSX9nwXIBk5t9tuQetrlsGQ3aIYVsat'
access_token = '1390628851705802754-PrwRNEfvVF6NwX07br8L9yQKF8oH8Q'
access_token_secret = 'obJyasMKNbRcr9GoipwjdKPjojIVCANvclLlmhZbZBywD'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#set the keyword and save to th database
def processdata(data):
    dict={}
    dict['id']=data['id_str']
    dict['key']='Australia'
    dict['doc']=data
    db.save(dict)

#define the listener
class LocateListener(StreamListener):

    def __init__(self):
        super().__init__()

    def on_data(self, data):
        tweetJson = json.loads(data, encoding= 'utf-8')
        print('1')
        # uif the tweet has geo information
        if tweetJson['geo']!=None or tweetJson['coordinates'] or tweetJson['place']:   
            #limit the speed  
            
            time.sleep(1)
            processdata(tweetJson)
        return True

    def on_error(self, status):
        print (status)

# connect the database
import couchdb
server = couchdb.Server('http://admin:admin@172.26.134.73:5984/')
try:
    db = server.create('twitter_streamer')
except:
    print('database already exist!')
    db = server['twitter_streamer']

listener = LocateListener()
stream = tweepy.Stream(auth,listener)
stream.filter(locations = [111,-44,155,-9])

