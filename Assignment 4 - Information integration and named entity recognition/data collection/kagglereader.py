#!/usr/bin/python

import csv
import pymongo
import progressbar

movie_metadata = []

#Function to establish connection to MongoDB
def connect_mongo():
	client = pymongo.MongoClient("mongodb://clusterbigdata.placeholder.edu")
	db = client.Grupo04
	return db

#Reading dataset from csv file
with open('movie_metadata.csv', 'rb') as csvfile:
	dataset = csv.reader(csvfile, delimiter=',')
	#Extracting header names
	header =  dataset.next()
	for row in dataset:
		#For each row filling a JSON object with the respective information, casting to proper datatypes
		entry = {
			"color": 					row[0],
			"director_name":			row[1],
			"num_critic_for_reviews":	int(row[2]) if not row[2] == '' else row[2],
			"duration":					int(row[3]) if not row[3] == '' else row[3],
			"director_facebook_likes":	int(row[4]) if not row[4] == '' else row[4],
			"actor_3_facebook_likes":	int(row[5]) if not row[5] == '' else row[5],
			"actor_2_name":				row[6],
			"actor_1_facebook_likes":	int(row[7]) if not row[7] == '' else row[7],
			"gross":					int(row[8]) if not row[8] == '' else row[8],
			"genres":					str(row[9]).split('|'),
			"actor_1_name":				row[10],
			"movie_title":				unicode(row[11], 'UTF-8').replace(u'\xa0', u''),
			"num_voted_users":			long(row[12]),
			"cast_total_facebook_likes":long(row[13]),
			"actor_3_name":				row[14],
			"facenumber_in_poster":		int(row[15]) if not row[15] == '' else row[15],
			"plot_keywords":			str(row[16]).split('|'),
			"movie_imdb_link":			row[17],
			"num_user_for_reviews":		int(row[18]) if not row[18] == '' else row[18],
			"language":					row[19],
			"country":					row[20],
			"content_rating":			row[21],
			"budget":					int(row[22]) if not row[22] == '' else row[22],
			"title_year":				int(row[23]) if not row[23] == '' else row[23],
			"actor_2_facebook_likes":	int(row[24]) if not row[24] == '' else row[24],
			"imdb_score":				float(row[25]),
			"aspect_ratio":				float(row[26]) if not row[26] == '' else row[26],
			"movie_facebook_likes":		int(row[27]) if not row[27] == '' else row[27]
		}
		movie_metadata.append(entry)

db = connect_mongo()
number_elements = len(movie_metadata)
# Progressbar to show progress
bar = progressbar.ProgressBar(maxval=number_elements, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
bar.start()
number_elements = 0
for entry in movie_metadata:		
	db.metadata.insert_one(entry)
	bar.update(number_elements+1)
bar.finish()

