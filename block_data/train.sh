#!/bin/bash

echo "Starting train script for block data"


echo "Reading realsense depths..."
echo 
sleep 1

python3 utils/read_realsense_depth.py --base_repo_path block_data

echo "Reading touch depths..."
echo 
sleep 1

python3 utils/read_touch_depths.py --base_repo_path block_data


echo "Fusing vision and touch..."
echo 
sleep 1

# python3 utils/fuse_touch_vision.py --root_dir 'block_data' --aligning_depths 'realsense_depths' --touch_depth 'touch_depth' --zoe_depth_path 'blocks_zoe_depth' --vision_output_dir 'vision' --fused_output_dir 'fused_output_dir' --touch_var 'touch_var'

python3 utils/fuse_touch_vision.py --root_dir 'block_data' --aligning_depths 'realsense_depths' --touch_depth 'touch_depth' --zoe_depth_path 'blocks_zoe_depth' --use_uncertainty --vision_output_dir 'vision' --fused_output_dir 'fused_output_dir' --touch_var 'touch_var'

echo "Adding depths and uncertainties to transforms.json..."
echo 
sleep 1

python3 utils/add_depth_file_path_to_transforms.py --base_repo_path block_data --filename 'transforms.json' --depth_file_path_template 'fused_output_dir' --uncertainty_file_path_template 'fused_output_dir_uncertainty'