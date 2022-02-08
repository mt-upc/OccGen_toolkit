import cld3
import glob
import json
import nltk
import sys
import os
import re

def readJSON(file):
	with open(file) as f:
		json_file = json.load(f)
	return json_file

def writeTextFile(file, data):
	with open(file, 'a') as f:
		for sentence in data:
			if sentence != '' and sentence != "\n": f.write(sentence.strip() + "\n")

def tokenization(sentence, lg):
	sentences = []
	
	if language == "sw":
		sentences = nltk.sent_tokenize(sentence, language="english")
	elif language == "en":
		sentences = nltk.sent_tokenize(sentence, language="english")
	#TODO: requirements
	elif language == "af":
		sentences=ar_split.corenlp_ssplitter(ar_tokenizer, sentence)
	#TODO: requirements
	elif language == "ru":
		sentences = nltk.sent_tokenize(sentence, language="russian")
	
	return sentences

def languageDetection(sentence, lg, text):
	langauge_detected = cld3.get_language(sentence).language
	# Language detection constraint
	if language == langauge_detected:
		text.add(sentence)
	else:
		print(langauge_detected, language, sentence)

	return text

def main(input_path, output_path):

	files = glob.glob(input_path + "*.json")
	# Creating arabic object
	# ar_tokenizer = ar_split.CoreNLPTokenizer()

	for file in files:
		occupation = readJSON(file)

		for entity in occupation:

			try:
				os.mkdir(output_path + entity + "/")
			except:
				continue

			for language in occupation[entity]:
				
				text = set() # removes duplicate local sentences

				for sentence in occupation[entity][language]:
					language = language.replace("https://","")	
					language = language.split(".wikipedia.org")[0]
					
					sentences = tokenization(sentence, language)

					for sentence in sentences:
						text = languageDetection(sentence, language, text)

				try:
					writeTextFile(output_path + entity + "/" + language + ".txt", text)
				except:
					break