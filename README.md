# Touch-GS Data
Official Dataset and Preprocessing Module for Touch-GS: Visual-Tactile Supervised 3D Gaussian Splatting


![Results](image.png)

Structure of each Dataset


```
- imgs: All images for train and test
- train.sh: Main training script 
- touches: Raw touches (not used in this repo). Contains raw images from the DenseTact optical tactile sensor and depths.
- transforms.json: Contains camera poses and paths to files and depth/uncertainties.
- realsense_depth/s: Realsense sensor depths
- gpis_depth/var: Raw results from the GPIS 
- touch_depth/var: Depths and variances from touch
- <scene>_zoe_depth: list of depths after running monocular depth
- vision_baseline: Baseline depths (aligned) for training a 3D-GS
- vision: Aligned vision
- zoe_depth_aligned: (not needed) as is
- fused_output_dir/uncertainty: Fused results with our method.
```
