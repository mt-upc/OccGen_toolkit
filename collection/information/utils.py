from SPARQLWrapper import SPARQLWrapper, JSON

import json
import sys

def read_json(file):
    with open(file) as f:
        json_file = json.load(f)
    return json_file

def write_json_2_file(file, data):
	with open(file, 'w', encoding='utf8') as outfile:
		json.dump(data, outfile, ensure_ascii=False)

def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()
