import tweepy
import json
import random
import nltk
import dateutil.parser as parser

# English stopwords from NLTK Library
stopwords = nltk.corpus.stopwords.words('english')
topics = ['strangerthings2', 'riverdale', 'mindhunter', 'netflix']


def flattenJSON(user, iso):
    dictionary = dict()
    # Converting created time to iso format
    dictionary["created_at"] = parser.parse(user["created_at"]).isoformat()[:-6] + '.' + str(
        random.randint(1, 1000)) + 'Z'
    # Get the country iso code
    dictionary["iso_code"] = iso
    # Get the tweet country
    dictionary["country"] = user["place"]["country"]
    dictionary["hashtags"] = []
    dictionary["topic"] = []
    # Loop to get a list of hastags and determine the topic
    for i in range(len(user["entities"]["hashtags"])):
        tag = user["entities"]["hashtags"][i]["text"]
        if tag.lower() in topics:
            dictionary["topic"].append(tag.lower())
        elif tag.lower() == 'strangerthingss2':
            dictionary["topic"].append('strangerthings2')
        dictionary["hashtags"].append(tag)
    # Get the favorite count
    dictionary["favorite_count"] = user["favorite_count"]
    # Get the language of the tweet
    dictionary["lang"] = user["lang"]
    # Get the retweet count
    dictionary["retweet_count"] = user["retweet_count"]
    # Split the text by space
    tokens = user["text"].split(" ")
    dictionary["text"] = []
    # Loop to get the words in the tweet excluding hashtags and stopwords
    for i in range(len(tokens)):
        if tokens[i] != "" and not tokens[i].startswith('#') and not tokens[i] in stopwords:
            dictionary["text"].append(tokens[i])
    # Get the followers count
    dictionary["followers_count"] = user["user"]["followers_count"]
    # Get the friend count
    dictionary["friends_count"] = user["user"]["friends_count"]
    # Get the statuses count
    dictionary["statuses_count"] = user["user"]["statuses_count"]
    return dictionary


# Twitter credentials can be obtained from Twitter dev
consumer_key = 'XXX'
consumer_secret = 'XXX'
access_key = 'XXX'
access_secret = 'XXX'

# Commands to handle authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=False)

# Open file that contains country codes for querying by country
cFile = open('country_codes-new.json')
# Open file containing iso codes for each country
iFile = open('isocodes.json')

country_id = json.loads(cFile.read())
country_iso = json.loads(iFile.read())

# Query terms
query = '#Netflix OR #StrangerThings2 OR #Mindhunter OR #Riverdale OR #StrangerThingsS2'
start = 'place:'

count = 0

# Main loop to get tweets
for country, countryID in country_id.items():
    iso = country_iso[country]
    errorCount = 0
    searchQuery = start + countryID + ' ' + query
    # Cursor object that gets the tweets based on query
    users = tweepy.Cursor(api.search, q=searchQuery).items()
    while True:
        try:
            # Loop through the users
            user = next(users)
            count += 1
        except tweepy.TweepError:
            # catches TweepError when rate limiting occurs, then restarts
            user = next(users)
        except StopIteration:
            break
        try:
            # Get the required fields
            newJson = flattenJSON(user._json, iso)
            print(json.dumps(newJson))

        except UnicodeEncodeError:
            errorCount += 1
            print("UnicodeEncodeError,errorCount =" + str(errorCount))
