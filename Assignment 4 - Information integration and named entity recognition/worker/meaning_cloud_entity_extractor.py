# Este es otro entity extractor que me parecio interesante
# detecta mas topics que el anterior, podriamos mirar este
# para intentar obtener el nombre de las peliculas tambien.
# La unica restriccion es el numero de peticiones que se hacen
# desde una misma ip (2000 por hora)

import requests

url = 'http://api.meaningcloud.com/topics-2.0'
token = 'b9496d2133ad2838c5463f96024a132e'

def extract_entities(text):

	payload = 'key='+ token +'&lang=en&txt=' + text + '&tt=a'
	headers = {'content-type': 'application/x-www-form-urlencoded'}

	response = requests.request("POST", url, data=payload, headers=headers)

	return response.text
