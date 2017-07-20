#!flask/bin/python
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import requests
import pymongo

app = Flask(__name__)
CORS(app,resources=r'/*')

client = pymongo.MongoClient("mongodb://clusterbigdata.placeholder.edu")
#client = pymongo.MongoClient()
db = client.Grupo04

@app.route('/movies/search',methods=['POST'])
def retrieve_movies_data():

	response = {}
	response['list'] = []

	text = request.json['text']

	response['list'] = list(db.questions.find(
		{"summary":{"$regex":text}},{"_id":0,"summary":1,"entities.entity_list.resume":1}).limit(100))

	return jsonify(response),200

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)
