#!/bin/bash

#macbook air
# FILE_PATH="/home/qubuntu/Git/qlin2021/catkin_ws/src/qlin_control/README.md"
# FILE_PATH="/home/qubuntu/Git/qlin2021/catkin_ws/src/qros_module/README.md"

#PC
# FILE_PATH="/home/quentinlin/Github/qlin2021/catkin_ws/src/qros_module/qlin_robot_switch_manager/README.md"
# FILE_PATH="/home/quentinlin/Github/qlin2021/catkin_ws/src/qlin_control/README.md"



# FILE_PATH="test_file/README_nomark.md"
FILE_PATH="test_file/README_proc.md"
# FILE_PATH="test_file/README_toc.md"

FILE_PATH="README.md"


OUTPUT_FILE="README.md"


python toc_convert.py --input-file "${FILE_PATH}" --output-file "${OUTPUT_FILE}"


# python toc_convert.py --input-file "${FILE_PATH}" --output-file "${OUTPUT_FILE}" --location-identifier [TOCC]
