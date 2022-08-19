""" Usage:
    <file-name> --src=IN_FILE --target=OUT_FILE --no_splits=numeric_value --split=one_for_split_zero_for_merge
"""
# External imports
from distutils.dir_util import copy_tree
from distutils.file_util import move_file
import os

from docopt import docopt

def split_into_folders(input_path, output_path, folders):
	dirs = os.listdir(input_path)

	dirs = list(filter(lambda x: x[0] == "Q", dirs)) # ensure only dirs related to wikidata item 
	print(dirs)
	[os.mkdir(output_path + str(folder) + "/") for folder in range(folders)]

	for i, dir in enumerate(dirs):
		os.mkdir(output_path + str(i%folders) + "/" + dir)
		copy_tree(input_path + dir, output_path + str(i%folders) + "/" + dir) 

def merge_into_folder(input_path, output_path, folders):

	for i in range(folders):	# for each folder
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
	# Parse command line arguments
	args = docopt(__doc__)

	src_folder = args["--src"]
	target_folder = args["--target"]
	num_splits = int(args["--no_splits"])
	split_or_merge = int(args["--split"]) #true if split, false if merge

	print(split_or_merge)

	# in this case, src is "../data/preprocessing/" and trg is "../data/mining/"
	if split_or_merge==1:
		split_into_folders(src_folder, target_folder, num_splits)
	
	elif split_or_merge==0: #in this case src is "../data/mining/", target is "../data/alignment/"
		merge_into_folder(src_folder, target_folder , num_splits)

	
	# mining/mining.py --src="/home/usuaris/scratch/christine.raouf.saad/En-Es/" --target="../data/mining/" --no_splits=10  split=0