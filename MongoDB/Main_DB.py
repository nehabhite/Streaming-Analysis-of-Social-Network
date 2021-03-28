import argparse
import globals
from streaming_Data import TwitterStreamer

LOCAL_DB = globals.LOCAL_CLIENT.twitter_data

class LoadDatabase():

    def __init__(self, batch_size, limit):
        self.batch_size = batch_size
        self.buffer = []
        self.limit = limit
        self.counter = 0

    def load_tweets(self, tweet):

        self.buffer.append(tweet)
        print(tweet['text'])
        if self.limit - self.counter < self.batch_size:
            self.batch_size = self.limit - self.counter
        if len(self.buffer) >= self.batch_size:
            LOCAL_DB.tweet_dicts.insert_many(self.buffer)
            print(f'\n ----Loaded tweets into local DB----')
            self.buffer = []
            self.counter += self.batch_size

def populate_database(batch_size, limit, keywords):
    callback_function = LoadDatabase(batch_size, limit).load_tweets
    twitter_streamer = TwitterStreamer(keywords)
    twitter_streamer.stream_tweets(limit, callback_function)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Fetching tweets and load into local DB')

    parser.add_argument('-k', '--keyword_list',
                        nargs='+',
                        help='<Required> Enter any keywords to be searched in streamed tweets.',
                        required=True)

    parser.add_argument('-b', '--batch_size',
                        type=int,
                        default=2,
                        help='No. of tweets fetched per batch?')

    parser.add_argument('-n', '--total_number',
                        type=int,
                        default=10,
                        help='Total number of tweets?')

    args = parser.parse_args()

    print(f"\nLoading tweets for \" {args.keyword_list} \" into Local DB...\
          \nWait for progress status...\n\n")
    populate_database(args.batch_size, args.total_number, args.keyword_list)
