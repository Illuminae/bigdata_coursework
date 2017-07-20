#!/usr/bin/python

import pymongo
import feedparser
import re

#Define function to parse an RSS feed
def get_rss_from_url(news_url):
	feed = feedparser.parse(news_url)
	return feed

#Function to establish connection to MongoDB
def connect_mongo():
	client = pymongo.MongoClient("mongodb://clusterbigdata.placeholder.edu")
	db = client.Grupo04
	return db

#function to read recent question rss from movies.stackexchange.com
def retrieve_stackexchange_data(db):
	questions = get_rss_from_url("https://movies.stackexchange.com/feeds")
	for question in questions.entries:
		if db.questions.find({'id' : question.id}).count() == 0:
			question.pop("updated_parsed")
			question.pop("published_parsed")
			db.questions.insert_one(question)

print('Opening database connection.....')
db = connect_mongo()
print('Initiating retrieval of Stackexchange data.....')
retrieve_stackexchange_data(db)