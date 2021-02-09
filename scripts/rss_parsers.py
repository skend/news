import xmltodict
import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup

# FINANCIAL TIMES
def ft(content):
    d = convert_xml_to_dict(content)['rss']['channel']
    data = d['item']

    for item in data:
        if d['title'] == 'News Feed':
            item['section'] = 'general'
        else:
            item['section'] = d['title'].lower()

        item['url'] = item['link']
        item['source'] = 'ft'
        item['date'] = datetime.strptime(item['pubDate'], "%a, %d %b %Y %H:%M:%S %Z")
        item.pop('link', None)
        item.pop('guid', None)
        item.pop('pubDate', None)
        # soup = get_soup(item['link'])
        # img = soup.select('.main-image img')

    return data



def convert_xml_to_dict(input):
    return xmltodict.parse(input)


def get_soup(url):
    res = requests.get(url)
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(res.text)
    return BeautifulSoup(res.text, features="html.parser")