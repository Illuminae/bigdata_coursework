#!flask/bin/python
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import requests

app = Flask(__name__)
CORS(app,resources=r'/*')

@app.route('/uniandesdata',methods=['GET'])
def retrieve_uniandes_data():
	url = 'http://127.0.0.1:5000/uniandesdata'
	crawl_url = 'http://127.0.0.1:5000/uniandesdata/crawl'	
	res = requests.get(url)
	requests.get(crawl_url)
	return jsonify(res.json()),200

@app.route('/mashup/rss1',methods=['POST'])
def retrieve_rss1():

	response = {
		"nofilter":[
			{"title":"titulo 1"},{"title":"titulo 2"},{"title":"titulo3"}
		],
		"regex":[
			{"title":"titulo 1"},{"title":"titulo 2"},{"title":"titulo3"}
		],
		"xquery":[
			{"title":"titulo1","date":"2017-02-26","link":"www.google.com"},
			{"title":"titulo2","date":"2017-02-16","link":"www.facebook.com"},
			{"title":"titulo3","date":"2017-01-15","link":"www.youtube.com"},
		]
	}
	return jsonify(response),200

@app.route('/mashup/rss',methods=['POST'])
def retrieve_rss():
	res = requests.post('http://127.0.0.1:5000/mashup/rss',json=request.json)
	return jsonify(res.json()),200

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)
