#!/usr/bin/python

import datetime
import pymongo
import feedparser
import re


#Determining current day as the IMDB site does not return a date
now = datetime.datetime.now()

#Define function to parse an RSS feed
def get_rss_from_url(news_url):
	feed = feedparser.parse(news_url)
	return feed

#Function to establish connection to MongoDB
def connect_mongo():
	client = pymongo.MongoClient("mongodb://clusterbigdata.placeholder.edu")
	db = client.Grupo04
	return db

# Function to grab both IMDB RSS feeds, loop through their entries and write
# every entry to MongoDB
def retrieve_imdb_data(db):
	born_today = get_rss_from_url('http://rss.imdb.com/daily/born/')
	died_today = get_rss_from_url('http://rss.imdb.com/daily/died/')

	for date in born_today.entries:
		name = re.search(r'([A-Z]\S+ ){2,3}', date.summary)
		year = re.search(r'[0-9]+', date.summary)
		born_entry = {
			'name' : unicode(name.group()).strip(),
			'date' : str(now.day) + '/' + str(now.month) + '/' + year.group(),
			'type' : 'birth'
		}
		db.dates.insert_one(born_entry)

	for date in died_today.entries:
		name = re.search(r'([A-Z]\S+ ){2,3}', date.summary)
		year = re.search(r'[0-9]+', date.summary)
		died_entry = {
			'name' : unicode(name.group()).strip(),
			'date' : str(now.day) + '/' + str(now.month) + '/' + year.group(),
			'type' : 'death'
		}
		db.dates.insert_one(died_entry)

#Executing function
print('Opening database connection.....')
db = connect_mongo()
print('Initiating retrieval of IMDB data....')
retrieve_imdb_data(db)
