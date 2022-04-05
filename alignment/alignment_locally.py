import glob
import json
import sys
import csv
import os
import argparse
from builtins import int
from collection.information import utils


def loadPaths(path):
	tsv = glob.glob(path + "*.tsv")

	paths = []
	for path in tsv:
		filename = os.path.basename(path)
		lg = filename.split(".")[0].split("-")[0]
		paths.append((path, lg))

	return paths

#getting sentences as a set from a tsv doc to intersect with others
def get_pivot_sentences(document, path):
	pivot_sentences = set()
	wrong_sentences = 0
	for row in document:
		try:
			pivot_sentences.add(row[2])
		except:
			wrong_sentences += 1
	#print("Wrong sentences: ", str(wrong_sentences) +' at '+ path)
	return pivot_sentences

def load_intersection(path):
	with open(path, encoding='utf8') as f:
		data = []
		map = {}
		for i,line in enumerate(f):
			data.append(line.strip())
			map[line.strip()] = i
	return data, map

def load_tsv_candidates(path):
	tsv_file = open(path)
	document = csv.reader(tsv_file, delimiter="\t")
	return document

def get_alignment_with_pivot_target(document, pivot_intersection):
	alignment = list()

	for row in document:
		try:
			if row[2] in pivot_intersection:
				alignment.append((row[0],row[1],row[2]))
		except:
			continue

	return alignment

def intersected_sentences(paths):
	pivot_intersection = set()

	for idx, path in enumerate(paths):
		document = load_tsv_candidates(path)
		pivot_sentences = get_pivot_sentences(document, path)

		if idx == 0:
			pivot_intersection = pivot_sentences
		else:
			pivot_intersection = pivot_intersection.intersection(pivot_sentences)

	return pivot_intersection

def add_alignment_information(alignment_information, alignments, language, intersection_map):
	alignment_wrong_sentences=0
	for alignment in alignments:
		try:
			similarity, src_stc, pivot_ln = alignment
			#pass the position
			position = intersection_map[pivot_ln]
			alignment_information[position][language] = {
				"sentence": src_stc,
				"pivot_similarity": similarity
			}
		except:
			alignment_wrong_sentences+=1

	return alignment_information


def init_alignment_information(alignment_information, intersection_map, pivot_ln):
	for key in intersection_map:
		alignment_information[intersection_map[key]]={
			pivot_ln:{
				"sentence": key,
			}
		}
	return alignment_information


def loop_directories(alignment_input_path, pivot_ln):


	for entity_id in os.listdir(alignment_input_path):
		alignment_dic = {}
		intersected_sent_entity = {}
		print('entity_id:'+ entity_id+'\n')
		if os.path.isdir(alignment_input_path + '/' + entity_id):
			tsv_list = glob.glob(alignment_input_path + '/' + entity_id + '/' + "*.tsv")
			intersected_sent_entity=intersected_sentences(tsv_list)
			#loop on set ..to have an index
			map = {}
			for ind,sen in enumerate(intersected_sent_entity):
				map[sen.strip()] = ind
			alignment_dic=init_alignment_information(alignment_dic, map, pivot_ln)
			paths = loadPaths(alignment_input_path  + '/' + entity_id + '/')
			print(paths)
			for cand_path, lg in paths:
				print(cand_path)
				document = load_tsv_candidates(cand_path)
				alignments = get_alignment_with_pivot_target(document, intersected_sent_entity)
				alignment_dic = add_alignment_information(alignment_dic, alignments, lg, map)

			#print(alignment_dic)
			if alignment_dic:
				utils.write_json_2_file( alignment_input_path + '/' + entity_id+'/'+'alignments.json', alignment_dic)
			print('finished entity:'+entity_id)
			print('**********************************************')




if __name__ == '__main__':
	#main(sys.argv[1], sys.argv[2],sys.argv[3], sys.argv[4])
	alignment_input_path='/home/christine/PycharmProjects/GENOCC/data/alignment'
	pivot_language='en'
	loop_directories(alignment_input_path, pivot_language)
