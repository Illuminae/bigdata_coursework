from flask import request
import io
import datetime

consecutive = 0

def get_consecutive():

	global consecutive
	consecutive += 1
	return consecutive

def process_key(key_element,place_search):
	
	node = {}
	node['id'] = str(get_consecutive())

	key_attributes = key_element.split(",")

	place = key_attributes[1].strip()
	node['caption'] = place
	node['role']='lugar'

	# filter by character name
	if place_search:
		if place_search.lower() not in place.lower():
			return None

	return node

def valid_date(init_date,end_date,date):

	# If element has no date then is a valid node
	if not date:
		return True

	#If no constraint dates were informed then is a valid node
	if not init_date and not end_date:
		return True


	valid = True

	try: 
		translated_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
	except ValueError:
		return True

	if init_date:
		translated_init_date = datetime.datetime.strptime(init_date, "%Y-%m-%d").date()
		if translated_date < translated_init_date:
			valid = False

	if end_date:
		translated_end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
		if translated_date > translated_end_date:
			valid = False

	return valid

def process_values(node_key,line_elements,edges_list,node_list,
	character,init_date,end_date):
	
	added = False

	for element in line_elements:

		key_attributes = element.split(",")

		if len(key_attributes) < 2:
			continue

		node_type = key_attributes[0].strip()
		name = key_attributes[1].strip()
		date = key_attributes[2].strip()

		# filter by character name
		if character:
			if character.lower() not in name.lower():
				continue

		# filter by date
		if not valid_date(init_date,end_date,date):
			continue

		node = {}
		node['id'] = str(get_consecutive())
		node['caption'] = name
		node['role']='persona'

		edge = {}
		edge['source'] = node['id']
		edge['target'] = node_key['id']
		edge['edgeType'] = 'Nacido_en'

		edges_list.append(edge)
		node_list.append(node)
		added = True

	return added


def process_line(node_list,edges_list,line,character,place_search,init_date,end_date):
		
		line_elements = line.split("|")

		node_key = process_key(line_elements[0],place_search)

		if not node_key:
			return

		added = process_values(node_key,line_elements[1:],
			edges_list,node_list,character,init_date,end_date)

		if added:
			node_list.append(node_key)

def process_file(filename, request):

	node_list = []
	edges_list = []

	character = request.json['persona']
	place_search = request.json['lugar']
	init_date = request.json['fechain']
	end_date = request.json['fechafin']

	with io.open(filename, "r", encoding="utf-8") as lines:
		for line in lines:
			process_line(node_list,edges_list,line,character,place_search,init_date,end_date)
			if len(node_list) > 2000:
				break

	response = {'nodes':node_list, 'edges': edges_list}

	return response

