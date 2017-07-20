import pymongo
import json
from bson.json_util import dumps


client = pymongo.MongoClient("mongodb://clusterbigdata.placeholder.edu")
db = client.Grupo04
tweet_list = []
file_path = './'
print "Iterating tweets.........."
for tweet in db.tweets.find({"polarity":{'$ne': None }}):
	tweet_list.append(tweet)

print "Successfully retrieved list with " + str(len(tweet_list)) + " tweets"

with open("tagged_data.json", "ab") as result_file:
	result_file.write(dumps(tweet_list))

print "Data is being saved to path " + file_path
