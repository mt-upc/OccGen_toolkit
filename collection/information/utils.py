from SPARQLWrapper import SPARQLWrapper, JSON

import json
import sys

#TODO: move this file to collection directory

def read_json(file):
    with open(file) as f:
        json_file = json.load(f)
    return json_file

def write_json_2_file(file, data):
	with open(file, 'w', encoding='utf8') as outfile:
		json.dump(data, outfile, ensure_ascii=False)

def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO: adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


# compute languages in an occupation and its related entities for further uses
def compute_lang_stats(occupations):
    occ_languages = {}
    occ_gender = {}
    occ_languages_entities = {}  # entities in the languag
    entities_info = {}
    stats_occ = 0
    for occupation in occupations:
        entities = occupations[occupation]
        for entity in entities:
            languages = occupations[occupation][entity]['languages']
            gender = occupations[occupation][entity]['gender']
            entities_info[entity] = occupations[occupation][entity]
            for language in languages:
                ln = language[0]
                # all these are not really languages
                if 'simple' not in ln and 'source' not in ln and 'quote' not in ln and 'common' not in ln and 'old' not in ln and 'news' not in ln and 'book' not in ln and 'voyage' not in ln and 'versity' not in ln:
                    ln = ln.replace('wiki', '')
                    if ln in occ_languages:
                        occ_languages[ln] += 1
                        occ_languages_entities[ln].append(entity)
                    else:
                        occ_languages[ln] = 1
                        occ_languages_entities[ln] = [entity]
            # filled in the last step
            if occ_languages and occ_languages_entities:
                if gender in occ_gender:
                    occ_gender[gender] += 1
                else:
                    occ_gender[gender] = 1
                stats_occ += 1

        return occupation, occ_languages, occ_languages_entities, occ_gender, entities_info, stats_occ


# gets id of occupation from the file name
def dic_occ_name(file):
    occ_id = file.split('/')[-1].replace('.json', '')
    data = read_json(file)
    occ_name = ''
    for occ in data:
        occ_name = occ
    return occ_name, occ_id
