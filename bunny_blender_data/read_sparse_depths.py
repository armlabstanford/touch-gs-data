import os
from PIL import Image
from matplotlib import pyplot as plt
import numpy as np

# Path to the directory containing depth images
directory_path = 'gt_depths_blender'

# Function to read a depth image
def read_depth_image(file_path):
    with Image.open(file_path) as img:
        depth_array = np.array(img) / 1000
    print(np.min(depth_array), np.max(depth_array))
    plt.imshow(depth_array)
    plt.show()
    return depth_array

# Dictionary to hold file names and their respective depth arrays
depth_images = {}

# Iterate through the directory and read each depth image
for filename in os.listdir(directory_path):
    if filename.endswith('.png'):
        file_path = os.path.join(directory_path, filename)
        depth_images[filename] = read_depth_image(file_path)

# Now depth_images dictionary contains all depth images
