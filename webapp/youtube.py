import json
import urllib.request
import string
import random
import os

API_KEY = os.environ['YT_API_KEY']
YT_API = 'https://www.googleapis.com/youtube/v3'

VIEW_RANGES = [lambda x: x in range(0, 4500), 
               lambda x: x in range(4500, 57000),
               lambda x: x >= 57000]

def call_api(url):
    webURL = urllib.request.urlopen(url)
    data = webURL.read()
    encoding = webURL.info().get_content_charset('utf-8')
    return json.loads(data.decode(encoding))

def fetch_examples(category, count=120):
    rnd_query = ''.join(random.choice(string.ascii_uppercase + string.digits)
                        for _ in range(random.randint(1, 5)))
    url = YT_API + "/search?key={}&maxResults={}&part=snippet&type=video&q={}".format(API_KEY,count,rnd_query)
    random_vids = call_api(url)

    vid_ids = ','.join(r['id']['videoId'] for r in random_vids['items'])

    url = YT_API + "/videos?key={}&part=statistics&id={}".format(API_KEY,vid_ids)
    random_vids = call_api(url)

    return [r['id'] for r in random_vids['items'] if
            ('viewCount' in r['statistics']) and
            VIEW_RANGES[category](int(r['statistics']['viewCount']))]
