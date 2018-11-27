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
            user_dict[user]["following"] = tweet["user"]["following"]
            user_dict[user]["recorded_tweets"] = 1
            user_dict[user]["retweet_count"] = tweet["retweet_count"]
            user_dict[user]["text"] = [tweet["text"]]
            # Add the used hashtags of the tweet
            hashtags = tweet["entities"]["hashtags"]
            user_dict[user]["hashtags"] = set([hashtags[i]["text"] for i in range(len(hashtags))])

        # The user is already added
        else:
            # Keep the maximum amount of followers/following
            user_dict[user]["followers"] = max(tweet["user"]["followers_count"], user_dict[user]["followers"])
            user_dict[user]["following"] = max(tweet["user"]["following"], user_dict[user]["followers"])
            user_dict[user]["recorded_tweets"] += 1
            user_dict[user]["retweet_count"] += tweet["retweet_count"]
            # Keep the text of the tweet
            user_dict[user]["text"].append(tweet["text"])
            hashtags = tweet["entities"]["hashtags"]
            user_dict[user]["hashtags"] |= set([hashtags[i]["text"] for i in range(len(hashtags))])

    # Transform retweet count into an average for all users
    for user in user_dict.keys():
        user_dict[user]["retweet_count"] /= user_dict[user]["recorded_tweets"]

    return user_dict

def feature_extraction(user_dict):
    """Features: retweet count, followers, following, tweet count, avr text length"""
    result_dict = {}
    for username in user_dict.keys():
        result_dict[username] = {}
        result_dict[username]["followers"] = user_dict[username]["followers"]
        result_dict[username]["tweet_count"] = user_dict[username]["recorded_tweets"]
        text_list = user_dict[username]["text"]
        word_count = 0
        for text in text_list:
            words = text.split(" ")
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







