import json
import requests
import datetime
import twitter
import pymongo
from pymongo import MongoClient

url = "https://gateway.watsonplatform.net/personality-insights/api"
username = "XXXXXXXXXXXXXXX"
password = "XXXXXXXXXXXXXXX"

api = twitter.Api(consumer_key='XXXXXXXXXXXXXXXXXXXXXXXXXXXX',
                      consumer_secret='XXXXXXXXXXXXXXXXXXX',
                      access_token_key='XXXXXXXXXXXXXXXXXXXXX',
                      access_token_secret='XXXXXXXXXXXXXXXXXXX'

justin="justinbieber"
plato="DailyPlato"

justin_tweets = api.GetUserTimeline(screen_name=justin, count=200)
plato_tweets = api.GetUserTimeline(screen_name=plato, count=200)

jtweets = []
for row in justin_tweets:
    jtweets.append(row.GetText())

jclean_tweets = ".".join(jtweets)
jtext = ''.join([i if ord(i) < 128 else ' ' for i in jclean_tweets])

ptweets = []
for row in plato_tweets:
    ptweets.append(row.GetText())

pstring = ".".join(ptweets)
ptext = ''.join([i if ord(i) < 128 else ' ' for i in pstring])


server_path = 'mongodb://<username>:<password>@candidate.59.mongolayer.com:10382/gus_test?replicaSet=set-5676e9f3bb2dcf52ab000fad'
client = MongoClient(server_path)
db = client.gus_test

result = db.tweets.remove({})

jinput = {"name": "Justin Bieber",
           "occupation": "Singer",
           "tweets": jtext,
           "date": datetime.datetime.utcnow()
           }

pinput = {"name": "Plato",
           "occupation": "Philosopher",
           "tweets": ptext,
           "date": datetime.datetime.utcnow()
           }

collection = db.tweets
jtweets_id = collection.insert(jinput)
ptweets_id = collection.insert(pinput)

stuff = db.tweets.find()
for doc in stuff:
    print doc['name']

cursor = db.tweets.find()
for document in cursor:
    if document['name'] == 'Justin Bieber':
        jtext = document['tweets']
    if document['name'] == 'Plato':
        ptext = document['tweets']

jresponse = requests.post(url + "/v2/profile",
                          auth=(username, password),
                          headers = {"content-type": "text/plain"},
                          data=jtext
                          )
presponse = requests.post(url + "/v2/profile",
                          auth=(username, password),
                          headers = {"content-type": "text/plain"},
                          data=ptext
                          )
jdata = json.loads(jresponse.text)
j_discipline = jdata['tree']['children'][0]['children'][0]['children'][1]['children'][4]['percentage']

pdata = json.loads(presponse.text)
p_discipline = pdata['tree']['children'][0]['children'][0]['children'][1]['children'][4]['percentage']

result = db.tweets.update_one(
    {"name": "Justin Bieber"},
    {
        "$set": {
            "self-discipline": j_discipline
        }
    }
)

presult = db.tweets.update_one(
    {"name": "Plato"},
    {
        "$set": {
            "self-discipline": p_discipline
        }
    }
)

####
stuff = db.tweets.find()
for doc in stuff:
    print doc['name']
    print doc['self-discipline']
