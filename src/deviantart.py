import requests
import random
import re
import pprint
import json
import csv
import html

class API:
    CLIENT_ID     = '5530'
    CLIENT_SECRET = '17fed08d1c413f2c0adcc02e323fc6c7'
    API_ROOT      = 'https://www.deviantart.com/api/v1/oauth2'

    def __init__(self):
        params = {
            'grant_type': 'client_credentials',
            'client_id': self.CLIENT_ID,
            'client_secret': self.CLIENT_SECRET
        }
        response = requests.get('https://www.deviantart.com/oauth2/token',
                            params=params)
        text_response = json.loads(response.text)
        self.ACCESS_TOKEN = text_response['access_token']

    def get(self, url, params={}):
        params['access_token'] = self.ACCESS_TOKEN
        resp = requests.get(url, params=params)
        return resp.text

    def fetch_popular(self):
        data = []
        params = {
            'timerange': '1month',
            'limit': 100,
        }
        for t in [ 'photography', 'digitalart', 'traditional']:
            params['category_path'] = t
            params['offset'] = 0
            results = []
            while len(results) < 500:
                print(params)
                url = '{}{}'.format(self.API_ROOT, '/browse/popular')
                response = json.loads(self.get(url, params=params))

                deviations = response['results']
                print(deviations)
                params['offset'] = response['next_offset']
                results += deviations
                if not response['has_more']:
                    break

            data += results
        random.shuffle(data)
        return data[:500]

    def fetch_deviation_comment(self, deviation_id):
        params = {
            'limit': 50
        }
        url = '{}{}{}'.format(self.API_ROOT, '/comments/deviation/',
                              deviation_id)
        r = self.get(url, params=params)
        return json.loads(r)['thread']

api = API()
popular_deviations = api.fetch_popular()
pp = pprint.PrettyPrinter(indent=2)
pp.pprint(popular_deviations[:10])

print('Got {} deviations'.format(len(popular_deviations)))

re_tag_cleaner = re.compile('<.*?>')
with open('res/corpus.csv', 'w') as csvfile:
    fields = ['url', 'title', 'comment', 'category', 'category_path']
    writer = csv.DictWriter(csvfile, fieldnames=fields,
                            extrasaction='ignore')
    writer.writeheader()
    cnt = 0
    for deviation in popular_deviations:
        comments = api.fetch_deviation_comment(deviation['deviationid'])
        data = { key: deviation[key] for key in fields if key in deviation }
        if data['category_path'].startswith('photography'):
            data['category'] = 'photography'
        if data['category_path'].startswith('digitalart'):
            data['category'] = 'digitalart'
        if data['category_path'].startswith('traditional'):
            data['category'] = 'traditional'
        data['comment'] = '\n'.join([html.unescape(re.sub(re_tag_cleaner, '',
                                                comment['body'])) for comment in
                          comments])
        pp.pprint(data)
        writer.writerow(data)
        cnt += 1
        print(cnt)
