#!/bin/bash
# bash script to mine for bitexts in the BUCC corpus
# Partition to submit to
#SBATCH -p veu
#SBATCH --gres=gpu:1
#SBATCH --mem=40G # Memory
#SBATCH --job-name=laser_local_mining_1
#SBATCH --ignore-pbs
#SBATCH -x veuc01
#SBATCH --output=laser_local_mining_q5_q9

# path to data/mining/0 
path_occ='YOUR_PATH_GOES_HERE'
#loop on occ path to get entities then on entities to get files
langs=("es")
trg="en"


#####################################################################
# encoder path for LASER and model_dir environment variables
model_dir="${LASER}/models"
encoder="${model_dir}/bilstm.93langs.2018-12-26.pt"
bpe_codes="${model_dir}/93langs.fcodes"



###################################################################
#
# Tokenize and Embed
#
###################################################################

Embed () {
  ll=$2
  #txt="$1.txt.${ll}"
  txt="$1.txt"
  echo 'text'
  echo $txt
  #enc="$1.enc.${ll}"
  enc="$1.enc"
  echo 'encode'
  echo $enc
  if [ ! -s ${enc} ] ; then
    cat ${txt} | python3 ${LASER}/source/embed.py \
      --encoder ${encoder} \
      --token-lang ${ll} \
      --bpe-codes ${bpe_codes} \
      --output ${enc} \
      --verbose
  fi
}


###################################################################
#
# Mine for bitexts
#
###################################################################

Mine () {
  path=$1
  l1=$2
  l2=$3
  cand="${path}/${l1}-${l2}.candidates.tsv"
  echo $cand
  echo ${path}/${l1}.txt
  echo ${path}/${l2}.txt
  if [ ! -s ${cand} ] ; then
    python3 ${LASER}/source/mine_bitexts.py \
       ${path}/${l1}.txt ${path}/${l2}.txt \
       --src-lang ${l1} --trg-lang ${l2} \
       --src-embeddings ${path}/${l1}.enc --trg-embeddings ${path}/${l2}.enc \
       --unify --mode mine --retrieval max --margin ratio -k 4  \
       --output ${cand} \
       --verbose \
       --gpu
  fi
}
#########################################################################
#main script
##########################################################################
for entity in "$path_occ"/*
do
  if [ -d "$entity" ]; then
        # if the occupation  is a directory
	  echo $entity
          #embedding english
          Embed $entity/$trg ${trg} ${encoder} ${bpe_codes}
          #here we get the entities folders
          for lang in ${langs[@]} ; do
            #here we get the language file
            echo $entity/$lang
            #embedding the other langugae
            Embed $entity/$lang ${lang} ${encoder} ${bpe_codes}
            Mine $entity ${lang} ${trg}
          done
  fi

done
