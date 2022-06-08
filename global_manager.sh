# Change to required languages, ISO language code
languages=("en","es")
# Data path from collection/, mining/ or alignment/ directory
data="../data/" 

# Change directory to collection
cd collection
languages="${data}languages/"
information="${data}information/" 
occupations="${data}occupations/" 
monolingual="${data}monolingual/"
preprocessing="${data}preprocessing/"

python3 manager.py -o "${occupations}" -i "${information}" -e "${entities}" -m "${monolingual}" -p "${preprocessing}" -l "${languages}" 
cd ../

# Change directory to mining
cd mining
temporal="${data}temporal/"
python3 mining.py -o "split" -p "${preprocessing}" -t "${temporal}" -f 4
cd ../

# Change directory to alignment
cd alignment 
for i in {1..4}; do
	sh laser_script.sh "${temporal}${i}/" languages[0] languages[1:] # TODO: Configure bash with passed parameters
done
wait  # waits for all child processes
cd ../

# Change directory to mining
cd mining
alignment="${data}alignment/"
python3 mining.py -o "merge" -t "${temporal}" -a "${alignment}" -f 4