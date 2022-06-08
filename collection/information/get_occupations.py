# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/
import utils

endpoint_url = "https://query.wikidata.org/sparql"

query = """PREFIX entity: <http://www.wikidata.org/entity/>
PREFIX property: <http://www.wikidata.org/prop/direct/>
SELECT DISTINCT ?subject ?subjectLabel ?predicateLabel ?object ?objectLabel
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
VALUES(?object) {(entity:Q12737077)}
VALUES(?predicate) {(property:P31)}
}"""


def main(write_path):
    results = utils.get_results(endpoint_url, query)
    utils.write_json_2_file(write_path, results["results"]["bindings"])