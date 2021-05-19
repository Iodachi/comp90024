import requests
import json
from datetime import datetime
import argparse
import time
import couchdb
from couchdb.client import Server

from datetime import datetime, timedelta

def get_time(elm):
    if '[' not in elm:
        date = datetime.strptime(elm, '%a-%b-%d-%H:%M:%S-+0000-%Y')
    else:
        date = datetime.strptime(elm, '[\"melbourne\",%Y,%m,%d]')
    return date

def next_date(date):
    delta = timedelta(days=1)
    date += delta
    if date.strftime('%d')[0] != '0' and date.strftime('%m')[0] != '0':        
        date_str = '[\"'+ 'melbourne' +'\",'+ date.strftime('%Y,%m,%d') +']'
    elif date.strftime('%d')[0] == '0' and date.strftime('%m')[0] != '0':   
        date_str = '[\"'+ 'melbourne' +'\",'+ date.strftime('%Y,%m,')+date.strftime('%d')[-1] +']'
    elif date.strftime('%d')[0] != '0' and date.strftime('%m')[0] == '0': 
        date_str = '[\"'+ 'melbourne' +'\",'+ date.strftime('%Y,')+date.strftime('%m')[-1]+date.strftime(',%d') +']'
    else:        
        date_str = '[\"'+ 'melbourne' +'\",'+ date.strftime('%Y,')+date.strftime('%m,')[-2:] +date.strftime('%d')[-1]+']'
    return date_str



secure_remote_server = Server('http://admin:admin@172.26.133.210:5984/')
<<<<<<< HEAD
db = secure_remote_server.create('melbourne20_21')
# parser = argparse.ArgumentParser(description='COMP90024 Project Scrape Research Data')
# parser.add_argument('--batch', type=int, default=100)
# parser.add_argument('--total', type=int, default=100)
# parser.add_argument('--startDate', type=str, default='[\"sydney\",2015,1,1]')
# parser.add_argument('--endDate', type=str, default='[\"sydney\",2015,12,31]')
# parser.add_argument('--url', type=str, default='http://45.113.232.90/couchdbro/twitter/_design/twitter/_view/summary')
=======
>>>>>>> 8d0ec3bdf5e3b0e0db46313f9157f41dd9841376

#db = secure_remote_server.create('melbourne2020')

parser = argparse.ArgumentParser(description='COMP90024 Project Scrape Research Data')
parser.add_argument('--batch', type=int, default=1000)
parser.add_argument('--total_forday', type=int, default=80000)
parser.add_argument('--startkey', type=str, default='[\"melbourne\",2020,12,1]')
parser.add_argument('--endkey', type=str, default='[\"melbourne\",2020,12,1]')

args = parser.parse_args()
# argsparser
url = 'http://couchdb.socmedia.bigtwitter.cloud.edu.au/twitter/_design/twitter/_view/summary'
<<<<<<< HEAD
BATCHSIZE = 1000
#该地区在sydney那里

params={'include_docs':'true','reduce':'false','start_key':'[\"melbourne\",2020,10,2]','end_key':'[\"melbourne\",2020,10,2]',"skip": "0", "limit": str(BATCHSIZE)}
TOTALSIZE = 80000
num = 0
tweetlist = []
while num<TOTALSIZE:
=======
BATCHSIZE = args.batch
tweet_perday = 10000
#该地区在sydney那里

>>>>>>> 8d0ec3bdf5e3b0e0db46313f9157f41dd9841376

start_key = args.startkey
end_key = args.endkey
date_str = start_key
serverName = 'melbourne20_21'

try:
    db = secure_remote_server['melbourne20_21']
except:
    print('database already exist!!')

params={'include_docs':'true','reduce':'false','start_key':start_key,'end_key':end_key,"skip": "0", "limit": str(BATCHSIZE)}
TOTALSIZE = args.total_forday

count = 1


while True:
    params['start_key'] = date_str
    params['end_key'] = date_str
    print(params['start_key'],params['end_key'])

<<<<<<< HEAD
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
            if (len(dataDict['text'].split(' '))>5):
                doc_id, doc_rev = db.save(dataDict)   
        except Exception as e:

            print(e)
            print("Cannot upload a well-formatted tweet to couchDB")
=======
    date = get_time(date_str)
    if date == datetime(2021,1,1):
        break

    num = 0
    params['skip'] = str(0)
    while num<TOTALSIZE:
        try:
            
            message=requests.get(url,params,auth=('readonly', 'cainaimeeshaLu4Lejoo9ooW4jiopeid'))
            num = num + BATCHSIZE
            temp = num
            params['skip'] = str(temp)
            
            dataset = message.json()
            tweetlst = dataset["rows"]
            print(str(num) + "Tweets scraped")
            count = 0
            for tweet in tweetlst:
                try:
                    if count%7 == 0:
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
                        a = dataDict['text'].split(' ')
                        if (len(a)>5):
                            doc_id, doc_rev = db.save(dataDict)
                    count += 1
                except Exception as e:
                    print(e)
                    print("Cannot upload a well-formatted tweet to couchDB")
        except:
            print(date_str,message)
            continue
    date_str = next_date(date)



>>>>>>> 8d0ec3bdf5e3b0e0db46313f9157f41dd9841376
