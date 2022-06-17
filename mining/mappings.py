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
    occupations_info = occupations_merge(occupations_path, alignment_path)

    occupations_per_entity = {}
    entity_alignment = {}
    entity_gender = {}

    for occupation in occupations_info.keys():
        for gender in occupations_info[occupation].keys():
            for entity in occupations_info[occupation][gender]:
                entity_alignment[entity] = occupations_info[occupation][gender][entity]
                entity_gender[entity] = gender
                if entity not in occupations_per_entity.keys():
                    occupations_per_entity[entity] = [occupation]
                else:
                    occupations_per_entity[entity].append(occupation)

    print(occupations_per_entity)
    occupations_hierarchy = {}

    for entity in occupations_per_entity.keys():
        gender = entity_gender[entity]
        size = len(occupations_per_entity[entity])
        if size not in occupations_hierarchy.keys():
            occupations_hierarchy[size] = {}
        print(entity)
        occupation = occupations_per_entity[entity]
        occupation.sort()
        occupation = " ".join(occupation)
        print(occupation)
        if occupation not in occupations_hierarchy[size].keys():
            occupations_hierarchy[size][occupation] = {"male":{},"female":{}}
        occupations_hierarchy[size][occupation][gender] = {entity:entity_alignment[entity]}

    balanced_data = {}
    for occ_num in occupations_hierarchy:
        for occ_id in occupations_hierarchy[occ_num]:
            print("occ id:", occ_id)
            genders = occupations_hierarchy[occ_num][occ_id]
            male_entities = len(genders["male"].keys())
            female_entities = len(genders["female"].keys())
            min_entities = min(male_entities, female_entities)
            male = extract_min_entities(genders["male"], min_entities)
            print("male:", male, len(male))
            female = extract_min_entities(genders["female"], min_entities)
            print("female:", female, len(female))
            if len(female) == 0: continue
            male_sentences = 0
            for entity in male:
                male_sentences += len(entity[1])
            female_sentences = 0
            for entity in female:
                female_sentences += len(entity[1])
            min_sentences = min(male_sentences, female_sentences)
            male_sentences = extract_min_sentences(male, min_sentences)
            print(male_sentences)
            female_sentences = extract_min_sentences(female, min_sentences)
            print(female_sentences)
            balanced_data[occ_id] = {"female": female_sentences, "male":male_sentences}

    print(balanced_data)

if __name__ == '__main__':
    main("../data/json/", "../data/alignment/")