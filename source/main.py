from pymongo import MongoClient
import preprocessing as pre
import classifier as cl
import pickle
import codecs

# Global constants
MONGO_HOST= 'mongodb://localhost/test'
WRITE_FEATURE_DICT = True

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


    feature_dict = pre.feature_extraction(user_dict)
    if WRITE_FEATURE_DICT:
        output_file = codecs.open(r"../data/users_with_aggregated_features.tab", mode="w", encoding="utf-8")
        first_key = feature_dict.keys()[0]
        features = feature_dict[first_key].keys()
        features.sort()
        features.append("advertiser")
        header = "username\t" + "\t".join(features)
        lines = [header]
        for username in feature_dict.keys():
            line_array = [username]
            for f in features:
                if f == "advertiser":
                    if cl.is_advertiser(user_dict[username]):
                        line_array.append("1")
                    else:
                        line_array.append("0")
                else:
                    line_array.append(str(feature_dict[username][f]))
            line = "\t".join(line_array)
            lines.append(line)
        output_string = "\n".join(lines)
        output_file.write(output_string)






