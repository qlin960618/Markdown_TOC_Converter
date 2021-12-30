#!/bin/bash

# FILE_PATH="/home/qubuntu/Git/qlin2021/catkin_ws/src/qlin_control/README.md"
FILE_PATH="/home/qubuntu/Git/qlin2021/catkin_ws/src/qros_module/README.md"

OUTPUT_FILE="README.md"


python toc_convert.py --input-file "${FILE_PATH}" --output-file "${OUTPUT_FILE}"
