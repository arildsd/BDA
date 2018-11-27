from pymongo import MongoClient
import pprint


MONGO_HOST= 'mongodb://localhost/test'

if __name__ == '__main__':
    client = MongoClient(MONGO_HOST)
    # Use test database. If it doesn't exist, it will be created.
    index = 2
    db = client.test
    data = db.black_friday_tweets.find()
    name = data[index]['user']['screen_name']
    print(name)
    print("Keys: ", str(data[index].keys()))
    pprint.pprint(data[index])