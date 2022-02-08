from information import utils
import requests
import glob

endpoint_url = "https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&props=sitelinks/urls&ids="

def parse(response, wikidata_id):
	languages = []
	
	try:	
		entity = response["entities"]
		data   = entity[wikidata_id]   
		links  = data["sitelinks"] 

		for link in links:
			info = (links[link]["site"], links[link]["url"])
			languages.append(info)
	except:
		pass

	return languages

def getLanguages(wikidata_id):
	response = requests.get(endpoint_url + wikidata_id)
	response_json = response.json()

	return parse(response_json, wikidata_id)

def main(data_path):
	files = glob.glob(data_path + "*.json")
	for file in files:
		data = utils.readJSON(file)

		for occupation in data:
			entities = data[occupation]
			for entity in entities:
				entities[entity]["languages"] = getLanguages(entity)

			utils.writeJSON2File(file, data)
			break
