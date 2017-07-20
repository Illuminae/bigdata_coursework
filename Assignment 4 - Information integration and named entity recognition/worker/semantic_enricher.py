import pymongo
import json
import db_pedia_client as dbp
import sys
import re
from decimal import *

#client = pymongo.MongoClient("mongodb://clusterbigdata.placeholder.edu")
client = pymongo.MongoClient()

db = client.Grupo04

def prepare_form(form):
	prepared_form = form.strip()
	prepared_form = re.sub('[^a-zA-Z0-9 \n]', '', prepared_form)
	return prepared_form.replace(' ','_')

def get_data_from_semantic_object(semantic_object):

	if semantic_object['type'] == 'uri':
		value = semantic_object['value'] 
		value = value.replace('http://dbpedia.org/resource/','')
		return value.replace('_',' ')

	if 'literal' in semantic_object['type']:
		return str(semantic_object['value'])

	return ''

def get_data_from_point(point):
	point = point.replace('POINT(','')
	point = point.replace(')','')
	point = point.replace(')','')
	coordinates = point.split()
	return coordinates[0],coordinates[1]

def enrich_person(entity):
	semantic_gold = dbp.get_semantic_data(prepare_form(entity['form']))
	
	resume = {}
	relatives = ''
	partners = ''

	for relation in semantic_gold['results']['bindings']:
		if relation['p']['value'] == 'http://dbpedia.org/property/relatives':
			relatives += get_data_from_semantic_object(relation['o']) + " | "
		if relation['p']['value'] == 'http://dbpedia.org/ontology/birthPlace':
			resume['birthplace'] = get_data_from_semantic_object(relation['o'])
		if relation['p']['value'] == 'http://dbpedia.org/ontology/birthDate':
			resume['birthdate'] = get_data_from_semantic_object(relation['o'])
		if relation['p']['value'] == 'http://dbpedia.org/property/partner':
			partners += get_data_from_semantic_object(relation['o']) + " | "
		if relation['p']['value'] == 'http://dbpedia.org/property/spouse':
			partners += get_data_from_semantic_object(relation['o']) + " | "

	#Type 0 for persons
	resume['type'] = 0
	resume['relatives'] = relatives
	resume['partners'] = partners
	resume['name'] = entity['form']

	entity['resume'] = resume

	return entity

def enrich_location(entity):
	semantic_gold = dbp.get_semantic_data(prepare_form(entity['form']))
	
	resume = {}

	for relation in semantic_gold['results']['bindings']:
		if relation['p']['value'] == 'http://dbpedia.org/ontology/capital':
			resume['capital'] = get_data_from_semantic_object(relation['o'])
		if relation['p']['value'] == 'http://dbpedia.org/ontology/country':
			resume['country'] = get_data_from_semantic_object(relation['o'])
		if relation['p']['value'] == 'http://www.w3.org/2003/01/geo/wgs84_pos#geometry':
			resume['lon'],resume['lat'] = get_data_from_point(relation['o']['value'])

	#Type 1 for locations
	resume['type'] = 1
	resume['name'] = entity['form']
	entity['resume'] = resume

	return entity

def enrich_organization(entity):
	
	semantic_gold = dbp.get_semantic_data(prepare_form(entity['form']))
	
	resume = {}

	for relation in semantic_gold['results']['bindings']:
		if relation['p']['value'] == 'http://dbpedia.org/ontology/type':
			resume['dbptype'] = get_data_from_semantic_object(relation['o'])
		if relation['p']['value'] == 'http://dbpedia.org/property/locationCity':
			resume['city'] = get_data_from_semantic_object(relation['o'])
		if relation['p']['value'] == 'http://dbpedia.org/property/locationCountry':
			resume['country'] = get_data_from_semantic_object(relation['o'])
	
	#Type 2 for organizations
	resume['type'] = 2
	resume['name'] = entity['form']
	resume['semtype'] = entity['sementity']['type']
	entity['resume'] = resume

	return entity

def process_entity_by_semantic_id(entity):
	sementity_type = entity['sementity']['type']
	
	if sementity_type.startswith('Top>Person'):
		return enrich_person(entity)

	if sementity_type.startswith('Top>Location'):
		return enrich_location(entity)

	if sementity_type.startswith('Top>Organization'):
		return enrich_organization(entity)

	return entity

def process_entity_list(entity):
	if entity['sementity'].has_key('type'):
		return process_entity_by_semantic_id(entity) 
	
def process_question(question):
	question['entities']['entity_list'] = [process_entity_list(entity) for entity 
		in question['entities']['entity_list']]
	return question
	
def enrich_entities():

		questions = db.questions.find()

		questions = [process_question(q) for q in questions]
		
		for question in questions:
			db.questions.save(question)
			'''
			for entity in question['entities']['entity_list']:
				if entity.has_key('resume'):
					print ('---------------------------------')
					print entity['resume']
			'''
enrich_entities()