#!/bin/bash

echo "Starting train script for block data"

python3 utils/read_realsense_depth.py --base_repo_path block_data


python3 utils/read_touch_depths.py --base_repo_path block_data
