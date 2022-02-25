from collection.information import utils
import numpy as np
from functools import reduce
import glob
import argparse


def if_occ_has_list_lan(languages_in_occ, list_languages):
    occ_has_list = True
    for ln in list_languages:
        if (ln not in languages_in_occ):
            occ_has_list = False
            break

    return occ_has_list

# intersection between lists
def compute_common_entites(occupation, list_languages):
    list_entities = ()
    for ln in list_languages:
        entities_ln = occupation[ln]
        list_entities = list_entities + (entities_ln,)

    intersect = reduce(np.intersect1d, list_entities)
    list_entities_intersection = []
    for entity in intersect:
        list_entities_intersection.append(entity)
    return list_entities_intersection


###gender specifications
##customized to male and female
# todo: apply to more than binary
# we are applying filtering to male and female, it can be extended to genders
def filter_ln(occupation):
    male_filtered = False
    female_filtered = False
    if (occupation['male'] == 0):
        male_filtered = True

    elif (occupation['female'] == 0):
        female_filtered = True

    return male_filtered, female_filtered


def min_male_female(occupation):
    min_value = ''
    if occupation['male'] > occupation['female']:
        min_value = 'female'
    elif occupation['male'] <= occupation['female']:
        min_value = 'male'

    return min_value, min(occupation['male'], occupation['female'])


def filtered_male_female(source):
    male_filtered_language = []
    female_filtered_language = []

    for occ in source:
        male_filtered, female_filtered = filter_ln(source[occ])
        if male_filtered:
            male_filtered_language.append(occ)

        elif female_filtered:
            female_filtered_language.append(occ)
    return male_filtered_language, female_filtered_language


# removing those occupation unbalanced in male and female gender
def filter_unbalanced_occ(occ_entities, occ_entities_numbers, occ_entities_common_genders):
    filtered_list = []
    male_filtered_language, female_filtered_language = filtered_male_female(occ_entities_common_genders)

    if male_filtered_language:
        filtered_list = male_filtered_language
    if female_filtered_language:
        filtered_list += female_filtered_language

    # removing these occupations from our occ_entities lists
    if (filtered_list):
        for instance in filtered_list:
            occ_entities_filtered = occ_entities.pop(instance)
            occ_entities_numbers_filtered = occ_entities_numbers.pop(instance)
            occ_entities_common_genders_filtered = occ_entities_common_genders.pop(instance)

    return occ_entities, occ_entities_numbers, occ_entities_common_genders


def get_entities_links(list_languages_wiki, occ_entities, entities_info, write_path):
    occ_entity_ln = {}
    for occ in occ_entities:
        occ_entity_ln[occ] = {}
        for entity in occ_entities[occ]:
            languages = entities_info[entity]['languages']
            link_list = []
            for ln in languages:
                if ln[0] in list_languages_wiki:
                    link_list.append(ln[1])
            occ_entity_ln[occ][entity] = link_list
    utils.writeJSON2File(write_path, occ_entity_ln)


# todo, test for monolingual (we never tested for) maybe the intersection fails!
def get_languages_specified_output(occ_path, list_languages):
    files = glob.glob(occ_path + "*.json")
    occ_languages_all = {}
    occ_languages_entities_all = {}
    entities_info_all = {}
    list_occ_with_languages = []
    # we get from this step the occupation with its languages and for each language list of entities
    for file in files:
        occ_name, occ_id = utils.dic_occ_name(file)
        data = utils.readJSON(file)
        occupation, occ_languages, occ_languages_entities, gender, entities_info, stats_number = utils.computeLangStats(
            data)
        if occ_languages:
            occ_languages_all[occ_id] = occ_languages  # source_occ_lan  occ_lan.json
        if occ_languages_entities:
            occ_languages_entities_all[occ_id] = occ_languages_entities  # source_entities occ_lan_entities.json
        if entities_info:
            entities_info_all.update(entities_info)  # source_entities_info
        # if the occupation has the languages we want
        available = if_occ_has_list_lan(occ_languages, list_languages)
        if available:
            list_occ_with_languages.append(occ_id)

    # should be edited to the normal names
    count = 1
    occ_entities = {}
    occ_entities_numbers = {}
    occ_entities_common_genders = {}
    # compute the intersection of entities among given languages
    for occ in occ_languages_entities_all:
        if occ in list_occ_with_languages:
            print(occ)
            occ_entities_common_genders[occ] = {}
            intersection = compute_common_entites(occ_languages_entities_all[occ], list_languages)
            print(intersection)
            if len(intersection) != 0:
                occ_entities[occ] = intersection
                # this is to keep track of the number of entities in the occupation
                occ_entities_numbers[occ] = len(intersection)
                for entity in intersection:
                    gender = entities_info_all[entity]['gender']
                    if gender in occ_entities_common_genders[occ]:
                        occ_entities_common_genders[occ][gender] += 1
                    else:
                        occ_entities_common_genders[occ][gender] = 1

                count += 1

    print(occ_entities_common_genders)

    # todo:filter with binary
    occ_entities, occ_entities_numbers, occ_entities_common_genders = filter_unbalanced_occ(occ_entities,
                                                                                            occ_entities_numbers,
                                                                                            occ_entities_common_genders)

    return occ_entities, occ_entities_numbers, occ_entities_common_genders, entities_info_all


# calling in shell
# $ python3 example.py --list a b c

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--start_json_path", help="Path to folder with occupations jsons")
    parser.add_argument("--list_languages", nargs="+", default=["en", "es"])
    parser.add_argument("--write_path", help="Path to alignment dictionary")

    args = parser.parse_args()
    read_path = args.start_json_path
    # list_languages, append every language with wiki for the wiki languages names
    list_languages = args.list_languages
    list_languages_wiki = []
    for lang in list_languages:
        list_languages_wiki.append(lang + 'wiki')
    write_path = args.write_path

    occ_entities, occ_entities_numbers, occ_entities_common_genders, entities_info = get_languages_specified_output(read_path, list_languages)
    get_entities_links(list_languages_wiki, occ_entities, entities_info, write_path)
