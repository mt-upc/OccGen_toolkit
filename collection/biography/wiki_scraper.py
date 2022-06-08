from SPARQLWrapper import SPARQLWrapper, JSON
from collections import deque
from bs4 import BeautifulSoup

import requests
import utils
import json
import time
import sys
import re

# TODO: UTF-8 encoding
def clean_expression(expresion):
	expresion = re.sub("[\(].*?[\)]", "", expresion)
	expresion = re.sub("[\[].*?[\]]", "", expresion)

	expresion = expresion.replace("\n","")
	expresion = expresion.strip()

	expresion = expresion.replace("\'","'")
	expresion = expresion.replace("\xa0"," ")

	return expresion

# return the text in a list of paragraphs
def get_wiki_intro(soup):

	intro_text = []
	paragraphs = 0
	for paragraph in soup.select('p'):
		text = paragraph.get_text()
		clean_text = clean_expression(text)
		if clean_text != "": intro_text.append(clean_text)
	
	return intro_text
	

def get_soup(url):                                                   # Try/Catch block to prevent Bad Content being processed.
	print(url)
	try:
		response = requests.get(url)    
		response.encoding = 'UTF-8' 				
		return  BeautifulSoup(response.text, "html.parser")       
	except:
		print("Error: Bad Content, skipping link. Do not stop.")
		return None                                                 # Return None if the URL could not be processed. The Crawler will understand.

# return the main text content in a wikipedia page given a name
def get_text(url):
	soup = get_soup(url)
	if soup is not None:
		text = get_wiki_intro(soup)
		return text
	else:
		return ""

def main(input_path, output_path):
	# read json file from command line (occ>entity>urls)
	data = utils.load_json_file(input_path)

	for occupation in data:
		multi_lingual = {}
		for entity in data[occupation]:
			multi_lingual[entity] = {}
			time.sleep(2)
			for language in data[occupation][entity]:
				text = get_text(language)
				multi_lingual[entity][language] = text
		# store json file with occupation (id) as a filename
		utils.write_json_2_file(output_path + occupation + ".json", multi_lingual)







