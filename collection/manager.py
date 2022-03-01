from languages_extraction.languages_specification import main as languages_main
from preprocessing.preprocessing import main as preprocessing_main 
from biography.wiki_scraper import main as biography_main
from information.pipeline import main as information_main

# TODO: Config file or program args provided by global manager (bash)
# These path might need to mkdir (bash) from the global manager
occupations_path = "../data/occupations.json"
data_path        = "../data/json/"
entity_links_path = "../data/languages/entities.json"
monolingual_path = "../data/monolingual/"
preprocessing_path = "../data/preprocessing/"

# change to required languages, ISO language code
languages_list = ["en", "es"]

print('....Information Extraction of Occupations and Entities....')
information_main(occupations_path, data_path)
print('....Filtering Entities of Languages....')
languages_main(data_path, languages_list, entity_links_path)
print('....Extracting the monolingual data....')
biography_main(entity_links_path, monolingual_path)
print('....Preprocessing Monolingual Data....')
preprocessing_main(monolingual_path, preprocessing_path)
