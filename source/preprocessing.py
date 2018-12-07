def _prune_text(text):
    prune_list = [".", ",", "!", "?", ";", ":"]
    for p in prune_list:
        text = text.replace(p, "")
    return text


def group_by_user(data):
    """
    Function for transforming raw json data per tweet into summarised data per user.

    :param data: A list of dictionaries. Each dictionary is a tweet. The data should only contain english language.
    :return: A dictionary of all the users with summarized data for each user. The summerized data is:
            followers, following, a list of text from the tweets,
    """
    user_dict = {}
    for tweet in data:
        user = tweet["user"]["name"]
        if user == "":
          continue
        # Make dict entry if it is a new user
        if user not in user_dict.keys():
            user_dict[user] = {}
            user_dict[user]["followers"] = tweet["user"]["followers_count"]
            user_dict[user]["friends_count"] = tweet["user"]["friends_count"]
            user_dict[user]["recorded_tweets"] = 1
            user_dict[user]["statuses_count"] = tweet["user"]["statuses_count"]
            user_dict[user]["listed_count"] = tweet["user"]["listed_count"]
            user_dict[user]["favourites_count"] = tweet["user"]["favourites_count"]
            user_dict[user]["text"] = [tweet["text"]]
            # Add the used hashtags of the tweet
            hashtags = tweet["entities"]["hashtags"]
            user_dict[user]["hashtags"] = set([hashtags[i]["text"] for i in range(len(hashtags))])

        # The user is already added
        else:
            # Keep the maximum amount of followers/following
            user_dict[user]["followers"] = max(tweet["user"]["followers_count"], user_dict[user]["followers"])
            user_dict[user]["favourites_count"] = max(tweet["user"]["favourites_count"], user_dict[user]["favourites_count"])
            user_dict[user]["recorded_tweets"] += 1
            # Keep the text of the tweet
            user_dict[user]["text"].append(tweet["text"])
            hashtags = tweet["entities"]["hashtags"]
            user_dict[user]["hashtags"] |= set([hashtags[i]["text"] for i in range(len(hashtags))])

    return user_dict

def feature_extraction(user_dict):
    """Features: retweet count, followers, following, tweet count, avr text length"""
    blacklisted_features = ["text", "hashtags"]
    result_dict = {}
    features = user_dict[user_dict.keys()[0]].keys()
    for username in user_dict.keys():
        result_dict[username] = {}
        for f in features:
            if f not in blacklisted_features:
                result_dict[username][f] = user_dict[username][f]

        text_list = user_dict[username]["text"]
        word_count = 0
        for text in text_list:
            pruned_text = _prune_text(text)
            words = pruned_text.split(" ")
            word_count += len(words)
        avr_words_pr_tweet = word_count/len(text_list)
        result_dict[username]["avr_words_pr_tweet"] = avr_words_pr_tweet
        retweet_count = 0
        for text in text_list:
            words = text.split(" ")
            if words[0] == "RT":
                retweet_count += 1
        result_dict[username]["retweet_count"] = retweet_count
    return result_dict







