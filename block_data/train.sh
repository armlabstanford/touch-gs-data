#!/bin/bash

echo "Starting train script for block data"

# python3 utils/read_realsense_depth.py --base_repo_path block_data


# python3 utils/read_touch_depths.py --base_repo_path block_data


python3 utils/fuse_touch_vision.py --root_dir 'block_data' --aligning_depths 'realsense_depths' --touch_depth 'touch_depth' --zoe_depth_path 'blocks_zoe_depth' --vision_output_dir 'vision' --fused_output_dir 'fused_output_dir' --touch_var 'touch_var'

# python3 utils/fuse_touch_vision.py --root_dir 'block_data' --aligning_depths 'realsense_depths' --touch_depth 'touch_depth' --zoe_depth_path 'blocks_zoe_depth' --viz --vision_output_dir 'vision' --fused_output_dir 'fused_output_dir' --touch_var 'touch_var'
