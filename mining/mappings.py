import glob
import json
import os

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
        occupations_hierarchy[size][occupation][gender] = entity_alignment[entity]

    print(occupations_hierarchy)

if __name__ == '__main__':
    main("../data/json/", "../data/alignment/")