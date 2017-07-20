#!flask/bin/python
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import requests
import file_processor as fp
import pymongo

app = Flask(__name__)
CORS(app,resources=r'/*')

client = pymongo.MongoClient("mongodb://clusterbigdata.placeholder.edu")
db = client.Grupo04

accounts = ["@AlvaroUribeVel","@petrogustavo","@HOLLMANMORRIS","@JuanManSantos","@JERobledo",
	"@EnriquePenalosa","@AndresPastrana_","@ginaparody","@German_Vargas","@DCoronell",
	"@VickyDavilaH","@FicoGutierrez","@IvanCepedaCast","@piedadcordoba","@DanielSamperO",
	"@fdbedout","@PirryTv","@cesaralo","@ClaudiaLopez","@PachoSantosC"]

@app.route('/twitter/polarity',methods=['GET'])
def retrieve_polarity_stats():

	response = {}
	response['list'] = []

	for account in accounts:

		pipeline = [
			{"$match" : {"text" : {"$regex":account}}},
			{"$project" : {"polarity" : 1}},
			{"$group" : {"_id" : "$polarity", "count" : {"$sum" : 1}}},
			{"$sort" : {"_id" : -1}}
		]

		account_data = {}

		for data in list(db.tweets.aggregate(pipeline)) :

			print (data)
			
			if data['_id'] == -2:
				account_data['menosdos'] = data['count']
			if data['_id'] == -1:
				account_data['menosuno'] = data['count']
			if data['_id'] == 0:
				account_data['neutro'] = data['count']
			if data['_id'] == 1:
				account_data['uno'] = data['count']
			if data['_id'] == 2:
				account_data['dos'] = data['count']
			
			account_data['name'] = account

		response['list'].append(account_data)

	return jsonify(response),200

@app.route('/twitter/sentiment',methods=['GET'])
def retrieve_sentiment_stats():
	
	response = {}
	response['list'] = []

	for account in accounts:

		pipeline = [
			{"$match" : {"text" : {"$regex":account}}},
			{"$project" : {"sentiment" : 1}},
			{"$group" : {"_id" : "$sentiment", "count" : {"$sum" : 1}}},
			{"$sort" : {"_id" : -1}}
		]

		account_data = {}

		for data in list(db.tweets.aggregate(pipeline)) :

			print (data)
			
			if data['_id'] == -1:
				account_data['menosuno'] = data['count']
			if data['_id'] == 0:
				account_data['neutro'] = data['count']
			if data['_id'] == 1:
				account_data['uno'] = data['count']
			
			account_data['name'] = account

		response['list'].append(account_data)

	return jsonify(response),200

@app.route('/twitter/example',methods=['GET'])
def retrieve_example_tweets():

	response = {}

	response['polarity-positive-objective'] = list(db.tweets.find({"polarity" : 2},{"text":1,"_id":0}).limit(10))
	response['polarity-positive-subjetive'] = list(db.tweets.find({"polarity" : 1},{"text":1,"_id":0}).limit(10))
	response['polarity-neutral'] = list(db.tweets.find({"polarity" : 0},{"text":1,"_id":0}).limit(10))
	response['polarity-negative-objective'] = list(db.tweets.find({"polarity" : -1},{"text":1,"_id":0}).limit(10))
	response['polarity-negative-subjetive'] = list(db.tweets.find({"polarity" : -2},{"text":1,"_id":0}).limit(10))

	response['sentiment-positive'] = list(db.tweets.find({"sentiment" : 1},{"text":1,"_id":0}).limit(10))
	response['sentiment-neutral'] = list(db.tweets.find({"sentiment" : 0},{"text":1,"_id":0}).limit(10))
	response['sentiment-negative'] = list(db.tweets.find({"sentiment" : -1},{"text":1,"_id":0}).limit(10))

	return jsonify(response),200

@app.route('/twitter/robots',methods=['GET'])
def retrieve_robots():

	response = {}

	pipeline = [
		{"$match" : {"text" : {"$regex":"RT @"}}},
		{"$project" : {"user.screen_name" : 1, "retweeted_status.user.screen_name": 1, }},
		{"$group" : {"_id" : { "possible_robot" : "$user.screen_name", "person" : "$retweeted_status.user.screen_name"}, "count" : {"$sum" : 1}}},
		{"$match" : {"count" : {"$gt" : 4}}},
		{"$sort" : {"count" : -1}}
	]

	response['robots-by-rt-to-same-account'] = list(db.tweets.aggregate(pipeline))

	response['robot-by-followers-and-favourites'] = list(db.tweets.find({"$and" : [
		{"text":{"$regex":"RT @"}},
		{"retweeted_status":{"$nin":[None]}},
		{"user.followers_count":{"$lt":10}},
		{"user.favourites_count":{"$gt":500}}]},
		{"user.screen_name":1,"user.followers_count":1,"user.favourites_count":1,"_id":0}))

	return jsonify(response),200

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)
