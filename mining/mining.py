from distutils.dir_util import copy_tree
import os

def main(input_path, output_path, folders):
	dirs = os.listdir(input_path)
	dirs = list(filter(lambda x: x[0] == "Q", dirs)) # ensure only dirs related to wikidata item 
	
	[os.mkdir(output_path + str(folder) + "/") for folder in range(folders)]

	for i, dir in enumerate(dirs):
		os.mkdir(output_path + str(i%folders) + "/" + dir)
		copy_tree(input_path + dir, output_path + str(i%folders) + "/" +dir)  # dst can be a folder; use shutil.copy2() to preserve timestamp


if __name__ == '__main__':
	main("../data/preprocessing/", "../data/mining/", 4)
