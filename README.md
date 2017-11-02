# Netflix-Twitter-Analyzer

Uses streaming data from twitter to do market analysis for Netflix shows.

NoSQL Database Used: Druid

GetTweets.py : Gets tweets from twitter for a particular query. Tweets are retrieved by country, the country geo codes used by Twitter are available in 'country_codes-new.json'. Each tweet is then processed, it takes all the necessary columns for analysis. It also tokenizes the tweet text and removes stopwords and hashtags. (This is done for text analysis) The processed tweet is then printed.

The printed tweet is then sent to Druid by sending a POST request to Tranquility. Before doing this, the ingestion spec has to be set for Tranquility. This is contained in the file 'server.json'.

The command for posting the request is:

python3 GetTweets.py | curl -XPOST -H'Content-Type: application/json' --data-binary @- http://localhost:8200/v1/post/netflix-stream
