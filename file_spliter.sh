#!/bin/bash

# A simple bash script to split a text file (i.e. line by line) into several small pieces evenly.
# Usage: ./file_splite.sh FILE_NAME NUM_CHUNK
# FILENAME specifies the file to split.
# NUM_CHUNK is the number of pieces you want to split.

set -o pipefail
set -o errexit
set -o nounset
LC_ALL=C

if [ $# -lt 2 ]
then
	echo "Usage: $0 FILE_NAME NUM_CHUNK"
	exit 1 
fi

file_name=$1
typeset -i num_chunk
num_chunk=$2

for((i=0; i<${num_chunk}; ++i))
do
	awk -F"\t" '{if((NR-1)%"'${num_chunk}'"=="'$i'") print $0;}' ${file_name} > ${file_name}.chunk_${i}
done
