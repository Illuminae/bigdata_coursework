#!flask/bin/python
from flask import Flask, jsonify, request
import urllib
import json
import time
import subprocess
import os
import threading
import glob
import re
import html.parser

app = Flask(__name__)

last_crawl_ts = 0
last_rss_save = 0

@app.route('/api/v1.0/tasks', methods=['GET'])
def get_tasks():
	return jsonify({'tasks':tasks})

@app.route('/uniandesdata',methods=['GET'])
def retrieve_uniandes_data():
	newest = min(glob.iglob('/home/estudiante/project/worker/services/crawler/*.json'),key=os.path.getctime) 
	print ("----------------------------")
	print (newest)
	print ("----------------------------")
	with open(newest) as data_file:    
		data = json.load(data_file)
	return jsonify(data),200

@app.route('/uniandesdata/crawl',methods=['GET'])
def crawl(): 
	t1 = threading.Thread(target=send_spider)
	t1.start()
	return ('',200)

@app.route('/mashup/rss',methods=['POST'])
def retrieve_rss():
	title = request.json['title']
	description = request.json['description']
	category = request.json['category']
	
	google_rss_tech_data = get_rss_from_url('https://news.google.com/news?cf=all&hl=es&ned=es_co&topic=t&output=rss','gt')
	google_rss_business_data = get_rss_from_url('https://news.google.com/news?cf=all&hl=es&ned=es_co&topic=b&output=rss','gb')
	google_rss_entertaiment_data = get_rss_from_url('https://news.google.com/news?cf=all&hl=es&ned=es_co&topic=e&output=rss','ge')

	mashable_rss_data = get_rss_from_url_direct('http://feeds.mashable.com/Mashable?format=xml')
	
	mashable_filtered = filter_by_category_mashable(mashable_rss_data)

	no_filter = get_no_filter(google_rss_tech_data,google_rss_business_data,google_rss_entertaiment_data,mashable_rss_data)
	
	regex_filter = get_regex_filter(google_rss_tech_data,google_rss_business_data,google_rss_entertaiment_data,mashable_rss_data,title,description,category)

	response = {"nofilter":no_filter,"regex":regex_filter}

	return jsonify(response),200

def send_spider():
	global last_crawl_ts
	minutes_from_last_crawl = (time.time() - last_crawl_ts) / 60
	
	if minutes_from_last_crawl > 2:
		last_crawl_ts = time.time() 
		spider_name = 'nephila'
		file_name = 'data' + str(time.time()) + '.json'
		os.chdir('/home/estudiante/project/worker/services/crawler')
		subprocess.call(['scrapy','crawl', spider_name,"-o",file_name])

def get_rss_from_url_direct(news_url):
	rss_request = urllib.request.Request(news_url)
	rss_response = urllib.request.urlopen(rss_request)
	return rss_response.read()

def get_rss_from_url(news_url,file_prefix):
	
	global last_rss_save
	minutes_from_last_rss_save = (time.time() - last_rss_save) / 60	

	newest = None
	
	if any(glob.iglob('/home/estudiante/project/worker/services/rss/' + file_prefix + '*')):
		newest = min(glob.iglob('/home/estudiante/project/worker/services/rss/' + file_prefix + '*'),key=os.path.getctime)
	
	if newest is None:
		rss_request = urllib.request.Request(news_url)
		rss_response = urllib.request.urlopen(rss_request)
		
		t1 = threading.Thread(target=save_rss(news_url,file_prefix))
		t1.start()
		
		return rss_response.read()
	else:
		data = ''
		with open(newest,'r',encoding='utf-8') as myfile:
			data = myfile.read()
	
		if minutes_from_last_rss_save > 2:
			t1 = threading.Thread(target=save_rss(news_url,file_prefix))
			t1.start()
		return data

def save_rss(news_url,file_prefix):
	os.chdir('/home/estudiante/project/worker/services/rss/')
	urllib.request.urlretrieve(news_url,file_prefix + str(time.time()))

def filter_by_category_mashable(data):
	response = ''
	items = re.findall(r'<item>(.*?)</item>',str(data))
	for item in items:
		if (
			re.search(r'.*<category>Business</category>.*',item) is not None or
			re.search(r'.*<category>Tech</category>.*',item) is not None or
			re.search(r'.*<category>Entertainment</category>.*',item) is not None
		):
			response += '<item>' + item + '</item>'
	return response

def get_no_filter(data_one,data_two,data_three,data_four):
	response = []

	get_titles(response,data_one)
	get_titles(response,data_two)
	get_titles(response,data_three)
	get_titles(response,data_four)

	return response

def get_regex_filter(data_one,data_two,data_three,data_four,title,description,category):

	data_one = filter_by_title_regex(data_one,title)
	data_two = filter_by_title_regex(data_two,title)
	data_three = filter_by_title_regex(data_three,title)
	data_four = filter_by_title_regex(data_four,title)

	data_one = filter_by_description_regex(data_one,description)	
	data_two = filter_by_description_regex(data_two,description)
	data_three = filter_by_description_regex(data_three,description)
	data_four = filter_by_description_regex(data_four,description)

	if category == 'Ciencia y Tecnolog':
		data_two = ''
		data_three = ''
		data_four = filter_by_category_regex(data_four,'Tech')
	
	if category == 'Business':
		data_one = ''
		data_three = ''
		data_four = filter_by_category_regex(data_four,'Business')
	
	if category == 'Entertainment':
		data_one = ''
		data_two = ''
		data_four = filter_by_category_regex(data_four,'Entertainment')

	response = []
	
	get_titles(response,data_one)
	get_titles(response,data_two)
	get_titles(response,data_three)
	get_titles(response,data_four)

	return response

def filter_by_title_regex(data,title):
	response = ''
	if title:
		items = re.findall(r'<item>(.*?)</item>',str(data))		
		for item in items:
			if re.search(r'.*<title>.*' + title + r'.*</title>.*',item) is not None:
				response += '<item>' + item + '</item>'
		return response
	else:
		return data

def filter_by_description_regex(data,description):
	response = ''
	if description:
		items = re.findall(r'<item>(.*?)</item>',str(data))
		for item in items:
			if re.search(r'.*<description>.*' + description + r'.*</description>.*',item) is not None:
				response += '<item>' + item + '</item>'
		return response
	else:
		return data

def filter_by_category_regex(data,category):
	response = ''
	if category:
		items = re.findall(r'<item>(.*?)</item>',str(data))
		for item in items:
			if re.search(r'.*<category>.*' + category + r'.*</category>.*',item) is not None:
				response += '<item>' + item + '</item>'
		return response
	else:
		return data

def get_titles(response,data):
	for title in re.findall(r'<title>(.*?)</title>', str(data)):
		response.append({'title':title})

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
