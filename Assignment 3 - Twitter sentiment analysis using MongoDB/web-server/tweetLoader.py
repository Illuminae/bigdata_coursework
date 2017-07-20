import pymongo
import json

file_path = '/home/estudiante/project/web-server/tweets/@VickyDavilaH.json'

def loadFile():
	with open(file_path) as data_file:
		file_str = data_file.read()
		file_str = '[' + file_str + ']'
		file_str = file_str.replace('}{','},{')
		return json.loads(file_str)

client = pymongo.MongoClient("mongodb://clusterbigdata.placeholder.edu")
db = client.Grupo04

tweets = loadFile()
for batch in tweets:
	for status in batch['statuses']:
		db.tweets.insert_one(status)
	
