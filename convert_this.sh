#!/bin/bash
#define input and output file
INPUT_FILE="README.md"
OUTPUT_FILE="README.md"


#run the program
python toc_convert.py --input-file "${INPUT_FILE}" --output-file "${OUTPUT_FILE}"
