import crypto_currency as crypto
import tweepy
from credentials import *
from time import sleep


def post_tweet(tweet):
    try:
        api.update_status(status=tweet)
    except tweepy.TweepError as e:
        print(e.reason)


if __name__ == '__main__':
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)

    crypto.init()

    while True:
        post_tweet(tweet=crypto.get_price())
        sleep(3600)
