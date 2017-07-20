import pymongo
from bson.objectid import ObjectId
import meaning_cloud_entity_extractor as ee
import json
import time

#client = pymongo.MongoClient("mongodb://clusterbigdata.placeholder.edu")
client = pymongo.MongoClient()
db = client.Grupo04

def extract_entities():

		questions = db.questions.find()

		for question in questions:
			time.sleep(1)
			entities = ee.extract_entities(question['summary'].encode('utf-8')).encode('utf-8')
			entity_json = json.loads(entities)
			db.questions.update({"_id" : ObjectId(question['_id'])},{"$set" : {"entities" : entity_json}})

extract_entities()