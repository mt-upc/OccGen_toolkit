from distutils.dir_util import copy_tree
from distutils.file_util import move_file

import argparse
import os

def split_into_folders(input_path, output_path, folders):
	dirs = os.listdir(input_path)
	dirs = list(filter(lambda x: x[0] == "Q", dirs)) # ensure only dirs related to wikidata item 
	
	[os.mkdir(output_path + str(folder) + "/") for folder in range(folders)]

	for i, dir in enumerate(dirs):
		os.mkdir(output_path + str(i%folders) + "/" + dir)
		copy_tree(input_path + dir, output_path + str(i%folders) + "/" + dir) 

def merge_into_folder(input_path, output_path, folders):

	for i in range(4):	# for each folder
		dirs = os.listdir(input_path + str(i))
		dirs = list(filter(lambda x: x[0] == "Q", dirs)) # ensure only dirs related to wikidata item 
		for dir in dirs:
			files = os.listdir(input_path + str(i) + "/" + dir)
			os.mkdir(output_path + dir)
			for file in files:
				if file[-3:] == "tsv": # LASER alignment file type 
					move_file(input_path + str(i) + "/" + dir + "/" + file, output_path + dir) 

def main():
	ap = argparse.ArgumentParser()
	
	ap.add_argument("-o", "--operation", type=str, help="operation to perform: split or merge")
	ap.add_argument("-p", "--preprocessing_path", type=str, help="path to preprocessing folder")
	ap.add_argument("-t", "--temporal_path", type=str, help="path to preprocessing folder")
	ap.add_argument("-a", "--alignment_path", type=str, help="path to alignment folder")
	ap.add_argument("-f", "--folders", type=int, help="number of folders")
	
	args = vars(ap.parse_args())
	if args["type"] == "split": split_into_folders(args["preprocessing_path"], args["temporal_path"], 4)
	elif args["type"] == "merge": merge_into_folder(args["temporal_path"], args["alignment_path"], 4)
	else: print("At mining: Invalid type.")


if __name__ == '__main__':
	main()





