import os
import pymongo
import requests
import json
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv(dotenv_path='../.env')
client = pymongo.MongoClient(os.getenv('DB_CONNECTION_STRING'))
db = client['db']['articles']


def get_next_chunk(skip, limit):
    return db.find().skip(skip).limit(limit)


def modify_res(item):
    item['_id'] = str(item['_id'])
    return item


def get_image_from_article(source, url):
    if source == 'ft':
        return get_ft_image(url)


def get_ft_image(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, features="html.parser")
    data = json.loads("".join(soup.find("script", {"type":"application/ld+json"}).contents))
    print(data)
    print(data['image']['url'])
    exit(0)


if __name__ == '__main__':
    size = 500
    limit = 500
    skip = 0
    chunk_count = 1

    while size == limit:
        print('------ GETTING CHUNK #' + str(chunk_count) + ' ------')
        size = 0

        chunk = get_next_chunk(skip, limit)

        for item in chunk:
            image_name = str(item['_id']) + '.jpg'

            get_image_from_article(item['source'], item['url'])

            item['img_name'] = image_name
            db.replace_one({ 'url': item['url'] }, item, upsert=True)
            size += 1

        skip += size

        print('------ FINISHED CHUNK - SIZE: ' + str(size) + ' ------')
        chunk_count += 1
