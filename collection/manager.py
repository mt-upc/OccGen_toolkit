from languages_extraction.languages_specification import main as languages_main
from preprocessing.preprocessing import main as preprocessing_main 
from biography.wiki_scraper import main as biography_main
from information.pipeline import main as information_main

import argparse
import os

def collect(args):
	print('....Information Extraction of Occupations and Entities....')
	if not os.path.isdir(occupations_path): os.mkdir(occupations_path)
	occupations_path += "occupations.json"
	if not os.path.isdir(information_path): os.mkdir(information_path)
	information_main(occupations_path, information_path)

	print('....Filtering Entities of Languages....')
	if not os.path.isdir(entity_links_path): os.mkdir(entity_links_path)
	entity_links_path += "entities.json"
	languages_main(information_path, languages, entity_links_path)

	print('....Extracting the monolingual data....')
	if not os.path.isdir(monolingual_path): os.mkdir(monolingual_path)
	biography_main(entity_links_path, monolingual_path)

	print('....Preprocessing Monolingual Data....')
	if not os.path.isdir(preprocessing_path): os.mkdir(preprocessing_path)
	preprocessing_main(monolingual_path, preprocessing_path)


def main():
	ap = argparse.ArgumentParser()
	
	ap.add_argument("-o", "--occupations_path", type=str, help="path to occupations folder")
	ap.add_argument("-i", "--information_path", type=str, help="path to information folder")
	ap.add_argument("-e", "--entity_links_path", type=str, help="path to entities folder")
	ap.add_argument("-m", "--monolingual_path", type=str, help="path to monolingual folder")
	ap.add_argument("-p", "--preprocessing_path", type=str, help="path to preprocessing folder")
	ap.add_argument("-l", "--languages", type=list, default=False, help="list of ISO language code")
	
	args = vars(ap.parse_args())	

	collect(args)


if __name__ == '__main__':
	main()



