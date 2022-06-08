# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/
import utils
import glob
import time

endpoint_url = "https://query.wikidata.org/sparql"

query = """PREFIX entity: <http://www.wikidata.org/entity/>
PREFIX property: <http://www.wikidata.org/prop/direct/>
SELECT DISTINCT ?objectLabel
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
VALUES(?subject) {(entity:REPLACE)}
VALUES(?predicate) {(property:P21)}
}
"""

def main(data_path):
    files = glob.glob(data_path + "*.json")
    for file in files:
        data = utils.read_json(file)

        for occupation in data:
            entities = data[occupation]
            time.sleep(2)
            for entity in entities:
                if "gender" not in entities[entity].keys():
                    gender_query = query.replace("REPLACE", entity)
                    try:
                        response = utils.get_results(endpoint_url, gender_query)
                        entities[entity]["gender"] = response['results']['bindings'][0]['objectLabel']['value']     # This assumes theres only one triple in the response
                    except:
                        entities[entity]["gender"] = None

            utils.write_json_2_file(file, data)

if __name__ == '__main__':
    main("data/json/")
