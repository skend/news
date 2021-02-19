import requests
import rss_parsers
import os
import pymongo
from jproperties import Properties
from dotenv import load_dotenv

def get_feeds():
    feeds_location = '../feeds.properties'
    p = Properties()
    with open(feeds_location, 'rb') as f:
        p.load(f, 'utf-8')
    return p


def send_to_parser(key, content):
    if key.startswith('ft'):
        return rss_parsers.ft(key, res.content)


load_dotenv(dotenv_path='../.env')
client = pymongo.MongoClient(os.getenv('DB_CONNECTION_STRING'))
db = client['db']['articles']

feeds = get_feeds()
keys = feeds.properties.keys()
for k in keys:
    print(k)
    res = requests.get(feeds.properties[k])
    data = send_to_parser(k, res.content)
    for d in data:
        db.replace_one({ 'url': d['url'] }, d, upsert=True)

# go through every article in the db and grab the main_img
