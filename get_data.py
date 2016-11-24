import tweepy

auth = tweepy.OAuthHandler("yBpNlv9EEjDcBFdA5oh3u98HE", "5axiFOehYpNKHJmxFEWDjHHfG04TOuqzKQX8S4xBe4Euq0F8Yw")
auth.set_access_token("346366186-yvVwU27EiLm2sjVj6o2XS2VzkZgQWOvcdVAwj3H4", "4opRwLBJGEcSAqzgWaDlZ0w3QyXIY40DgixO2x01zBIDa")

api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text.encode("utf-8"))