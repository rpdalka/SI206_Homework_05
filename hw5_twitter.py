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

#usage should be python3 hw5_twitter.py <username> <num_tweets>
username = sys.argv[1]
num_tweets = sys.argv[2]

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

#Code for Part 1:Get Tweets
base_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
params = {'screen_name':username, 'count':num_tweets}
json_file = requests.get(base_url, params, auth = auth).text
# not necessary for rest of hw ##############
#with open('tweet.json', 'w') as outfile:
#    json.dump(json_file, outfile, indent=4)
#############################################

#Code for Part 2:Analyze Tweets
all_tweet_text = ""
json_data = json.loads(json_file)
for json_item in json_data:
    all_tweet_text += (" " + json_item['text'])

tokens = nltk.word_tokenize(all_tweet_text)
freqDist = nltk.FreqDist(token for token in tokens if token.isalpha()
                            and token not in stopwords.words('english')
                            and "http" not in token
                            and "https" not in token
                            and "RT" not in token)

for word, frequency in freqDist.most_common(5):
    print(word + " " + str(frequency))



if __name__ == "__main__":
    if not consumer_key or not consumer_secret:
        print("You need to fill in client_key and client_secret in the secret_data.py file.")
        exit()
    if not access_token or not access_secret:
        print("You need to fill in this API's specific OAuth URLs in this file.")
exit()
