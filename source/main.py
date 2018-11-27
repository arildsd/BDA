from pymongo import MongoClient
import preprocessing as pre
import classifier as cl
import pickle

# Global constants
MONGO_HOST= 'mongodb://localhost/test'

if __name__ == '__main__':
    try:
        dict_file = open(r"../data/user_dict", "r")
        user_dict = pickle.load(dict_file)
        dict_file.close()
        print("Loaded user dict form file.")
    except:
        # Dict not created, make a new one
        client = MongoClient(MONGO_HOST)
        db = client.test
        data = db.black_friday_tweets.find({"lang": "en"})
        user_dict = pre.group_by_user(data)
        dict_file = open(r"../data/user_dict", "w")
        pickle.dump(user_dict, dict_file)
        dict_file.close()
        print("Made and saved user dict to file.")

    advertisers = cl.find_advertisers(user_dict)





