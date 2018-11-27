AD_WORDS = ["sale", "discount", "deal", "off", "offer", "savings", "save"]
AD_HASHTAGS = ["sale"]

def is_advertiser(user_data):
    matches = 0
    text_list = user_data["text"]
    for text in text_list:
        words = text.split(" ")
        for word in words:
            if word.lower() in AD_WORDS:
                # Positive match
                return True
            elif ('%' in word or "$" in word):
                return True


    hashtags = user_data["hashtags"]
    for h_tag in hashtags:
        if h_tag in AD_HASHTAGS:
            # Positive match
            return True
    # No matches on either hashtags or words
    return False

def find_advertisers(user_dict):
    result_dict = {}
    for username in user_dict.keys():
        if is_advertiser(user_dict[username]):
            result_dict[username] = user_dict[username]
    return result_dict
