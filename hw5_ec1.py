from requests_oauthlib import OAuth1
import json
import sys
import requests
import secret_data # file that contains OAuth credentials
import nltk # uncomment line after you install nltk
from nltk.corpus import stopwords

## SI 206 - HW
## COMMENT WITH:
## Your section day/time:
## Any names of people you worked with on this assignment:

#usage should be python3 hw5_twitter.py <username1> <username2> <num_tweets>
usernames = []
try:
    usernames.append(sys.argv[1])
    usernames.append(sys.argv[2])
    num_tweets = sys.argv[3]
except:
    usernames.append(input('First username to look up > '))
    usernames.append(input('Second username to look up > '))
    num_tweets = input('Number of tweets to look at > ')

consumer_key = secret_data.CONSUMER_KEY
consumer_secret = secret_data.CONSUMER_SECRET
access_token = secret_data.ACCESS_KEY
access_secret = secret_data.ACCESS_SECRET

#Code for OAuth starts
url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)
requests.get(url, auth=auth)
#Code for OAuth ends

#Write your code below:
#Code for Part 3:Caching
#Finish parts 1 and 2 and then come back to this

CACHE_FNAME_1 = "tweet_cache_user1.json"
CACHE_FNAME_2 = "tweet_cache_user2.json"
try:
    cache_file_1 = open(CACHE_FNAME_1, 'r')
    cache_contents_1 = cache_file_1.read()
    CACHE_DICTION_1 = json.loads(cache_contents_1)
    cache_file_1.close()
except:
    CACHE_DICTION_1 = {}

try:
    cache_file_2 = open(CACHE_FNAME_2, 'r')
    cache_contents_2 = cache_file_2.read()
    CACHE_DICTION_2 = json.loads(cache_contents_2)
    cache_file_2.close()
except:
    CACHE_DICTION_2 = {}

def get_request(baseurl, params, usernum):
    unique_id = baseurl + "?screen_name=" + usernames[usernum] + "&count=" + num_tweets

    if usernum == 0:
        if unique_id in CACHE_DICTION_1:
            print("Fectching data from chache for " + usernames[usernum] + "...")
            return CACHE_DICTION_1[unique_id]
        else:
            print("Making request for new data" + usernames[usernum] + "...")
            json_file = requests.get(unique_id, auth = auth).text
            CACHE_DICTION_1[unique_id] = json.loads(json_file)
            dumped_json_cache = json.dumps(CACHE_DICTION_1)
            fw = open(CACHE_FNAME_1,"w")
            fw.write(dumped_json_cache)
            fw.close()
            return CACHE_DICTION_1[unique_id]
    elif usernum == 1:
        if unique_id in CACHE_DICTION_2:
            print("Fectching data from chache for " + usernames[usernum] + "...")
            return CACHE_DICTION_2[unique_id]
        else:
            print("Making request for new data" + usernames[usernum] + "...")
            json_file = requests.get(unique_id, auth = auth).text
            CACHE_DICTION_2[unique_id] = json.loads(json_file)
            dumped_json_cache = json.dumps(CACHE_DICTION_2)
            fw = open(CACHE_FNAME_2,"w")
            fw.write(dumped_json_cache)
            fw.close()
            return CACHE_DICTION_2[unique_id]

#Code for Part 1:Get Tweets
print('USER1:', usernames[0])
print('USER2:', usernames[1])
print('TWEETS ANALYZED:', num_tweets)
base_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
params = [{'screen_name':usernames[0], 'count':num_tweets}, {'screen_name':usernames[1], 'count':num_tweets}]

all_tweet_text = []
json_data = []
all_tweet_words = []
for i in range(len(params)):
    all_tweet_text.append("")
    json_data.append(get_request(base_url, params[i], i))
    for json_item in json_data[i]:
        all_tweet_text[i] += (" " + json_item['text'])
    all_tweet_words.append(all_tweet_text[i].split())


common = []
total = (all_tweet_text[0] + " " + all_tweet_text[1]).split()
common_str = ""
unique = ["",""]
for n in range(len(all_tweet_words[0])):
    is_unique = True
    for m in range(len(all_tweet_words[1])):
        if all_tweet_words[0][n] == all_tweet_words[1][m]:
            is_unique = False
    if is_unique == True:
        unique[0] += (" " + all_tweet_words[0][n])
    if is_unique == False:
        common.append(all_tweet_words[0][n])

for n in range(len(all_tweet_words[1])):
    is_unique = True
    for m in range(len(all_tweet_words[0])):
        if all_tweet_words[1][n] == all_tweet_words[0][m]:
            is_unique = False
    if is_unique == True:
        unique[1] += (" " + all_tweet_words[1][n])

for x in range(len(common)):
    for y in range(len(total)):
        if common[x] == total[y]:
            common_str += (" " + common[x])


tokens_common = nltk.word_tokenize(common_str)
tokens_unique_1 = nltk.word_tokenize(unique[0])
tokens_unique_2 = nltk.word_tokenize(unique[1])
freqDist_unique = []
freqDist_common = nltk.FreqDist(token for token in tokens_common if token.isalpha()
                            and token not in stopwords.words('english')
                            and "http" not in token
                            and "https" not in token
                            and "RT" not in token)
freqDist_unique.append(nltk.FreqDist(token for token in tokens_unique_1 if token.isalpha()
                            and token not in stopwords.words('english')
                            and "http" not in token
                            and "https" not in token
                            and "RT" not in token))
freqDist_unique.append(nltk.FreqDist(token for token in tokens_unique_2 if token.isalpha()
                            and token not in stopwords.words('english')
                            and "http" not in token
                            and "https" not in token
                            and "RT" not in token))

five_top = []
for q in range(3):
    if q != 2:
        five_top.append("5 MOST FREQUENT UNIQUE WORDS from " + usernames[q] + ":")
        for word, frequency in freqDist_unique[q].most_common(5):
            five_top[q] += (" " + word + " (" + str(frequency) + ")")
        print(five_top[q])
    else:
        five_top.append("5 MOST FREQUENT COMMON WORDS:")
        for word, frequency in freqDist_common.most_common(5):
            five_top[q] += (" " + word + " (" + str(frequency) + ")")
        print(five_top[q])

if __name__ == "__main__":
    if not consumer_key or not consumer_secret:
        print("You need to fill in client_key and client_secret in the secret_data.py file.")
        exit()
    if not access_token or not access_secret:
        print("You need to fill in this API's specific OAuth URLs in this file.")
exit()
