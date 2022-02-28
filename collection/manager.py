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

information_main(occupations_path, data_path)
languages_main(data_path, ["en", "es"], entity_links_path) 
biography_main(entity_links_path, monolingual_path)
preprocessing_main(monolingual_path, preprocessing_path)
