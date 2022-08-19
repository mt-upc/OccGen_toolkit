import glob
import json
import os

def print_stats(occupations_hierarchy):
    print(occupations_hierarchy)
    ## preparing min stats ##
    for occ_num in occupations_hierarchy:
        for occ_id in occupations_hierarchy[occ_num]:
            #number of entities
            print(' number of male entities')
            print(len(occupations_hierarchy[occ_num][occ_id]['male']))
            for entity_id in occupations_hierarchy[occ_num][occ_id]['male']:
                print(' number of sentences per entity')
                print(len(occupations_hierarchy[occ_num][occ_id]['male'][entity_id]))

            print(' number of female entities')
            print(len(occupations_hierarchy[occ_num][occ_id]['female']))
            for entity_id in occupations_hierarchy[occ_num][occ_id]['female']:
                print(' number of sentences per entity')
                print(len(occupations_hierarchy[occ_num][occ_id]['female'][entity_id]))



def read_json(file):
    with open(file) as f:
        json_file = json.load(f)
    return json_file

def get_occupations(path):
    return glob.glob(path + "Q*.json")

def entity_in_alignment(entity_id, path):
    return os.path.isdir(path + str(entity_id))

def occupations_merge(occupations_path, alignment_path):
    occupations = get_occupations(occupations_path)
    print(occupations)
    occupations_info = {}
    for occupation in occupations:
        data = read_json(occupation)
        occupation_id = (occupation.split("/")[-1]).replace(".json", "")
        for name in data.keys():
            for entity_id in data[name]:
                entity = data[name][entity_id]
                gender = entity["gender"]
                if entity_in_alignment(entity_id, alignment_path):
                    entity_alignment = read_json(alignment_path + entity_id + "/alignments.json")
                    if occupation_id in occupations_info.keys():
                        print(occupation_id, entity_id)
                        occupations_info[occupation_id][gender][entity_id] = entity_alignment
                    else:
                        print(occupation_id, entity_id)
                        occupations_info[occupation_id] = {"male": {}, "female": {}}
                        occupations_info[occupation_id][gender][entity_id] = entity_alignment

    return occupations_info

def extract_min_entities(entities, minimum):
    min_entities = []
    for entity in entities:
        avg_sum = 0
        for sentence in entities[entity]:
           avg = []
           for language in entities[entity][sentence]:
               if "pivot_similarity" in entities[entity][sentence][language].keys():
                   avg.append(float(entities[entity][sentence][language]["pivot_similarity"]))
           avg = sum(avg)/len(avg)
           avg_sum += avg
        min_entities.append([avg_sum, {entity:entities[entity]}])
    min_entities.sort(key=lambda x: x[0], reverse=True)
    return min_entities[0:minimum]

def extract_min_sentences(data, minimum):
    min_sentences = []
    min_aux_sentences = []
    for element in data:
        entities = element[1]
        for entity in entities:
            entity_sentences = []
            for sentence in entities[entity]:
               avg = []
               for language in entities[entity][sentence]:
                   if "pivot_similarity" in entities[entity][sentence][language].keys():
                       avg.append(float(entities[entity][sentence][language]["pivot_similarity"]))
               avg = sum(avg)/len(avg)
               entity_sentences.append([avg, {entity:entities[entity][sentence]}])
            entity_sentences.sort(key=lambda x: x[0], reverse=True)
            min_sentences.append(entity_sentences[0])
            if len(entity_sentences) > 1: min_aux_sentences.append(entity_sentences[1:])
    remainer = minimum - len(min_sentences)
    min_aux_sentences.sort(key=lambda x: x[0], reverse=True)
    if remainer > 0: min_sentences.append(min_aux_sentences[0:remainer])
    return min_sentences

def main(occupations_path, alignment_path):
    o