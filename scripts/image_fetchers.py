# entire file is disgusting please refactor for your own

import os
import pymongo
import requests
import json
import boto3
import botocore
import base64
import io
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv(dotenv_path='../.env')
client = pymongo.MongoClient(os.getenv('DB_CONNECTION_STRING'))
db = client['db']['articles']
s3 = boto3.client('s3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('AWS_SECRET_KEY'))
bucket_name = os.getenv('BUCKET_NAME')
image_save_location = os.getenv('IMAGE_SAVE_LOCATION')


def get_next_chunk(skip, limit):
    return db.find().skip(skip).limit(limit)


def modify_res(item):
    item['_id'] = str(item['_id'])
    return item


def get_image_from_article(source, url, image_name):
    if source == 'ft':
        return get_ft_image(url, image_name)


def get_ft_image(url, image_name):
    print('GET: ' + str(url))
    res = requests.get(url)
    soup = BeautifulSoup(res.text, features="html.parser")
    data = json.loads("".join(soup.find("script", {"type":"application/ld+json"}).contents))

    try:
        if 'image' in data:
            img_url = data['image']['url']
            img_res = requests.get(data['image']['url'])
            file_ext = os.path.splitext(img_url)[-1].lower()
            content_type = 'image/jpeg'

            if file_ext == '.jpg' or file_ext == '.jpeg':
                content_type = 'image/jpeg'
            elif file_ext == '.png':
                content_type = 'image/png'
            else:
                print('Could not find file extension: ' + file_ext)
                return None

            filename = str(image_name) + file_ext
            p = os.path.join(image_save_location, filename)

            with Image.open(BytesIO(img_res.content)) as img:
                img.thumbnail((256,256))
                img.save(p)

                with open(p, "rb") as image:
                    f = image.read()
                    s3.upload_fileobj(BytesIO(bytearray(f)), bucket_name, filename, ExtraArgs={'ContentType': content_type, 'ACL': 'public-read'})

            os.remove(p)
            return filename
    except Exception as e:
        print("Could not find or save image")
        print(e)

    return None


def image_to_byte_array(image:Image):
  imgByteArr = BytesIO()
  image.save(imgByteArr, format=image.format)
  imgByteArr = imgByteArr.getvalue()
  return imgByteArr


def get_images():
    size = 500
    limit = 500
    skip = 0
    chunk_count = 1

    while size == limit:
        print('------ GETTING CHUNK #' + str(chunk_count) + ' ------')
        size = 0

        chunk = get_next_chunk(skip, limit)

        for item in chunk:
            image_name = get_image_from_article(item['source'], item['url'], item['_id'])
            item['img_name'] = image_name

            # only upload if file not found
            if image_name != None:
                try:
                    s3.head_object(Bucket=bucket_name, Key=image_name)
                except botocore.exceptions.ClientError:
                    if image_name != None:
                        db.replace_one({ 'url': item['url'] }, item, upsert=True)

            size += 1

        skip += size
        print('------ FINISHED CHUNK - SIZE: ' + str(size) + ' ------')
        chunk_count += 1

if __name__ == '__main__':
    get_images()
    # get_ft_image("https://www.ft.com/content/2abe8a36-94a9-4bd3-9cd0-78636f2aed06", "meme") # test
