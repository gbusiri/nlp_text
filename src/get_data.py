import html
import tweepy
import csv
import string
import utils
import random

auth = tweepy.OAuthHandler("yBpNlv9EEjDcBFdA5oh3u98HE", "5axiFOehYpNKHJmxFEWDjHHfG04TOuqzKQX8S4xBe4Euq0F8Yw")
auth.set_access_token("346366186-yvVwU27EiLm2sjVj6o2XS2VzkZgQWOvcdVAwj3H4", "4opRwLBJGEcSAqzgWaDlZ0w3QyXIY40DgixO2x01zBIDa")

api = tweepy.API(auth)

search_params = {
    "id": "Lovelyz_Global",
    "user_id": "Lovelyz_Global",
}

with open('res/corpus.csv','w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=utils.fields, extrasaction='ignore')
    writer.writeheader()
    cursor = tweepy.Cursor(api.user_timeline, **search_params)
    tweets = [tweet for tweet in cursor.items(500)]
    random.shuffle(tweets)
    for tweet in tweets:
        raw_text = tweet.text
        processed_text = html.unescape(''.join([ch for ch in raw_text if ch in
                                  string.printable]).strip())
        data = {
            'truncated': tweet.truncated,
            'processed_text': processed_text,
            'created_at': tweet.created_at
        }
        writer.writerow(data)
