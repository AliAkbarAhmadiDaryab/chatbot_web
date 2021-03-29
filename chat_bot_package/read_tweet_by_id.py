import tweepy
import json

if __name__ == '__main__':
    tweeter_keys = json.load(open('../config/keys.json', 'rb'))
else:
    tweeter_keys = json.load(open('config/keys.json', 'rb'))

auth = tweepy.OAuthHandler(tweeter_keys['API key'], tweeter_keys['API secret key'])
auth.set_access_token(tweeter_keys['Access token'], tweeter_keys['Access token secret'])
api = tweepy.API(auth)


def get_tweet(tweet_id):
    tweets = api.statuses_lookup([tweet_id])
    if not tweets == []:
        tweets = json.dumps(tweets[0]._json)
        tweets = json.loads(tweets)
        text = tweets['text']
        return text
    return None
