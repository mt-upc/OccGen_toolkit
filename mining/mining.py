from distutils.dir_util import copy_tree
from distutils.file_util import move_file
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


# TODO: Manager call
if __name__ == '__main__':
	split_into_folders("../data/preprocessing/", "../data/mining/", 4)
	merge_into_folder("../data/mining/", "../data/alignment/", 4)