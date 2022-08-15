from information import get_entities_for_occupations as Entities
from information import get_occupations as Occupations
from information import get_languages as Languages
from information import get_gender as Gender

def main(occupations_path, output_path):
	print("Extracting Occupations...")
	#Occupations.main(occupations_path)

	print("Extracting Entities...")
	#Entities.main(occupations_path, output_path)

	print("Extracting Languages...")
	Languages.main(output_path)

	print("Extracting Gender...")
	Gender.main(output_path)
