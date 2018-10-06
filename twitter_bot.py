from credentials import *
import tweepy

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


def tweet(tweet):
    try:
        api.update_status(status=tweet)
    except tweepy.TweepError as e:
        print(e.reason)


tweet(tweet='Hello, world!')
