from __future__ import print_function
import tweepy
import json
from pymongo import MongoClient
# assuming you have mongoDB installed locally
# and a database called 'test'
MONGO_HOST= 'mongodb://localhost/test'
WORDS = ["#BlackFriday2018"]  # This is an OR relation
CONSUMER_KEY = "GswhEJ7pwXIYkiQKUm71GeErx"
CONSUMER_SECRET = "5l4hSoixMaMt8xJxI9uIWZxwCuR9kcgwq7wypO07RWYNsId77S"
ACCESS_TOKEN = "1051882775933083649-KRspbd4tkoaUKpKu23PsRmKWfmpdhH"
ACCESS_TOKEN_SECRET = "pRPsAj6dSvwNPdzXctHotYEEeGfuvdnNHUx4DPMxwghdO"
STORE_DATA = True

#API retrival started at ~10:00 23 nov.

class StreamListener(tweepy.StreamListener):
    # This is a class provided by tweepy to access the Twitter Streaming API.
    def on_connect(self):
        # Called initially to connect to the Streaming API
        print("You are now connected to the streaming API.")

    def on_error(self, status_code):
        # On error - if an error occurs, display the error / status code
        print('An Error has occured: ' + repr(status_code))
        return False

    def on_data(self, data):
        # This is the meat of the script...it connects to your mongoDB and stores the tweet
        try:
            if STORE_DATA:
                client = MongoClient(MONGO_HOST)
                # Use test database. If it doesn't exist, it will be created.
                db = client.test


            # Decode the JSON from Twitter
            datajson = json.loads(data)

            black_friday_tweets = db.black_friday_tweets
            black_friday_tweets.insert_one(datajson)


            created_at = datajson['created_at']
            username = datajson['user']['screen_name']
            #for k in datajson.keys():
                #print("key:", str(k), "values:", datajson[k])

            print("Tweet collected at " + str(created_at) + " made by " + str(username))
        except:
            print("Failed to get tweet.")

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
# Set up the listener. The 'wait_on_rate_limit=True' is needed to help with Twitter API rate limiting.
listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True))
streamer = tweepy.Stream(auth=auth, listener=listener)
print("Tracking: " + str(WORDS))
streamer.filter(track=WORDS)



