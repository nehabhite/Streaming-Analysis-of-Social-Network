import json

from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener

import globals

LANGUAGES = ['en']

def get_geo_data(tweet):
    geo_data = []
    if tweet['place'] != None:
        try:
            geo_data.append(tweet['place']['full_name'])
            geo_data.append(tweet['place']['bounding_box']['coordinates'])
        except KeyError:
            geo_data.append(['KeyError'])

    return geo_data

def get_user_location(tweet):

    user_location = []
    if tweet['user']['location'] != None:
        try:
            user_location.append(tweet['user']['location'])
        except KeyError:
            user_location.append(['KeyError'])

    return user_location

def get_hashtags(tweet):

    hashtags = []
    if 'extended_tweet' in tweet:
        for hashtag in tweet['extended_tweet']['entities']['hashtags']:
            hashtags.append(hashtag['text'])
    elif 'hashtags' in tweet['entities'] and len(tweet['entities']['hashtags']) > 0:
        hashtags = [item['text'] for item in tweet['entities']['hashtags']]

    return hashtags

def get_tweet_dict(tweet):

    if 'extended_tweet' in tweet:
        text = tweet['extended_tweet']['full_text']
    else:
        text = tweet['text']

    geo_data = get_geo_data(tweet)
    user_location = get_user_location(tweet)
    hashtags = get_hashtags(tweet)

    tweet = {'id': tweet['id_str'],
             'tweet_created_at': tweet['created_at'],
             'text': text,
             'user': tweet['user']['screen_name'],
             'source': tweet['source'],
             'language': tweet['lang'],
             'user_description': tweet['user']['description'],
             'num_followers':tweet['user']['followers_count'],
             'user_statuses': tweet['user']['statuses_count'],
             'user_created_at': tweet['user']['created_at'],
             'hashtags': hashtags,
             'tweet_location': geo_data,
             'user_location': user_location,
             }
    return tweet

class TwitterAuthenticator():

    def authenticate(self):
        auth = OAuthHandler(globals.CONSUMER_API_KEY, globals.CONSUMER_API_SECRET)
        auth.set_access_token(globals.ACCESS_TOKEN, globals.ACCESS_TOKEN_SECRET)
        return auth

class TwitterListener(StreamListener):


    def __init__(self, limit, callback):
        super().__init__() # Inherit __init__ method from parent class.
        self.limit = limit
        self.counter = 0
        self.callback = callback

    def on_error(self, status):

        if status == 420:
            return 420
        print(status)

    def on_data(self, data):

        t = json.loads(data)

        is_tweet_reply = t['in_reply_to_status_id'] == None
        is_quote = t['is_quote_status'] == False

        if 'RT' not in t['text'] and is_tweet_reply and is_quote:

            tweet = get_tweet_dict(t)
            self.callback(tweet)

            self.counter += 1

            if self.counter == self.limit:
                return False

class TwitterStreamer():

    def __init__(self, keywords):
        self.twitter_authenticator = TwitterAuthenticator()
        self.keywords = keywords

    def stream_tweets(self, limit, callback):
        listener = TwitterListener(limit, callback)
        auth = self.twitter_authenticator.authenticate()
        stream = Stream(auth, listener)
        stream.filter(track=self.keywords, languages=LANGUAGES)


if __name__ == "__main__":

    twitter_streamer = TwitterStreamer(['covid'])
    twitter_streamer.stream_tweets(10, print)

