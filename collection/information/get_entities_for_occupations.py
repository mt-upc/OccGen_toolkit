# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/
from information import utils

endpoint_url = "https://query.wikidata.org/sparql"

query = """PREFIX entity: <http://www.wikidata.org/entity/>
PREFIX property: <http://www.wikidata.org/prop/direct/>
SELECT DISTINCT ?subject ?subjectLabel
WHERE
{
?property rdf:type wikibase:Property .
?subject ?predicate ?object.
?property ?ref ?predicate.
?property rdfs:label ?predicateLabel.
?subject rdfs:label ?subjectLabel.
?object rdfs:label ?objectLabel.
FILTER (LANG(?subjectLabel) = 'en').
FILTER (LANG(?predicateLabel) = 'en').
FILTER (LANG(?objectLabel) = 'en').
VALUES(?object) {(entity:REPLACE)}
VALUES(?predicate) {(property:P106)}
}"""

# saving the results in dictionary in case we need easy access some time later
# a json file is saved for each entity
def getResultsEntity(occupations, write_path):

	for occupation_id, occupation_name in occupations:
		rdf_dict = {}

		occupation_query = query.replace("REPLACE", occupation_id)
		try:
			rdf = utils.getResults(endpoint_url, occupation_query)
			rdf_dict[occupation_name] = {}

			for entity in rdf['results']['bindings']:
				try:
					entity_id   = entity['subject']['value'].split("/")[-1]
					entity_name = entity['subjectLabel']['value']
					rdf_dict[occupation_name][entity_id] = {"name": entity_name}
				except:
					continue
		except:
			continue

		utils.writeJSON2File(write_path + occupation_id + ".json", rdf_dict)
		break

def getOccupationsRelatedEntities(read_path):
	data = utils.readJSON(read_path)

	occupations =[]
	for entry in data:
		occupation_id   = entry['subject']['value'].rsplit('/', 1)[-1]
		occupation_name = entry['subjectLabel']['value']
		occupations.append((occupation_id, occupation_name))

	return occupations

def main(read_path, write_path):
	occupations = getOccupationsRelatedEntities(read_path)
	getResultsEntity(occupations, write_path)





