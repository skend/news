import requests
import rss_parsers
import pprint
import pymongo
from jproperties import Properties
from dotenv import load_dotenv

def get_feeds():
    feeds_location = './feeds.properties'
    p = Properties()
    with open(feeds_location, 'rb') as f:
        p.load(f, 'utf-8')
    return p


def send_request(url):
    return requests.get(url)


def send_to_parser(key, content):
    if key.startswith('ft'):
        return rss_parsers.ft(res.content)


def send_to_db(data):
    if db.count_documents({"url": data['url']}) == 0:
        db.insert_many(data)


load_dotenv(dotenv_path='../.env')
client = pymongo.MongoClient(os.getenv('DB_CONNECTION_STRING'))
db = client['db']['articles']

pp = pprint.PrettyPrinter()
feeds = get_feeds()
keys = feeds.properties.keys()
for k in keys:
    res = send_request(feeds.properties[k])
    data = send_to_parser(k, res.content)
    send_to_db(data)