import requests
import json
from datetime import datetime
import argparse
import time
import couchdb
from couchdb.client import Server

secure_remote_server = Server('http://admin:admin@172.26.133.210:5984/')
db = secure_remote_server.create('melbourne_2020')
# parser = argparse.ArgumentParser(description='COMP90024 Project Scrape Research Data')
# parser.add_argument('--batch', type=int, default=100)
# parser.add_argument('--total', type=int, default=100)
# parser.add_argument('--startDate', type=str, default='[\"sydney\",2015,1,1]')
# parser.add_argument('--endDate', type=str, default='[\"sydney\",2015,12,31]')
# parser.add_argument('--url', type=str, default='http://45.113.232.90/couchdbro/twitter/_design/twitter/_view/summary')

# argsparser
url = 'http://couchdb.socmedia.bigtwitter.cloud.edu.au/twitter/_design/twitter/_view/summary'
BATCHSIZE = 100
#该地区在sydney那里

params={'include_docs':'true','reduce':'false','start_key':'[\"melbourne\",2020,1,1]','end_key':'[\"melbourne\",2020,12,31]',"skip": "0", "limit": str(BATCHSIZE)}
TOTALSIZE = 100000
num = 0
tweetlist = []
while num<TOTALSIZE:

    message=requests.get(url,params,auth=('readonly', 'cainaimeeshaLu4Lejoo9ooW4jiopeid'))


    num = num + BATCHSIZE
    
    temp = num
    params['skip'] = str(temp)
    # Message to dict
    dataset = message.json()

    # retrive all tweets
    tweetlst = dataset["rows"]
    print(str(num) + "Tweets scraped")
    for tweet in tweetlst:
        try:
            dataDict = {}
            dataDict["id"] = tweet["id"]
            dataDict["user"] = tweet["doc"]["user"]["screen_name"]
            dataDict["user_id"] = tweet["doc"]["user"]['id']
            dataDict["text"] = tweet["doc"]["text"]
            if tweet["doc"]["created_at"] != None:
                stringTime = tweet["doc"]["created_at"]
                dataDict["date"] = datetime.strptime(stringTime,'%a %b %d %H:%M:%S %z %Y').strftime('%Y-%m-%d %H:%M:%S%z')
                dataDict['Create_data'] = stringTime
            else:
                dataDict["date"] = ""
            dataDict["hashtags"] = []
            if tweet["doc"]["entities"]["hashtags"] != None:
                listHashtags = tweet["doc"]["entities"]["hashtags"]
                for hashtag in listHashtags:
                    if "text" in hashtag.keys():
                        dataDict["hashtags"].append(hashtag["text"])



            if tweet["doc"]["coordinates"]!= None and tweet["doc"]["coordinates"]["coordinates"] != None:
                dataDict["geo"] = tweet["doc"]["coordinates"]["coordinates"]	

            elif tweet["doc"]["geo"]!= None and tweet["doc"]["geo"]["coordinates"] != None:

                temp = tweet["doc"]["geo"]["coordinates"]
                if len(temp) == 2:
                    dataDict["geo"] = [temp[1], temp[0]]

            else:
                dataDict["geo"] = []
            dataDict['retweet'] = tweet["doc"]['retweet_count']
            dataDict['favorite'] = tweet['doc']['favorite_count']
            dataDict['language'] = tweet['doc']['lang']
            doc_id, doc_rev = db.save(dataDict)   
        except Exception as e:

            print(e)
            print("Cannot upload a well-formatted tweet to couchDB")
