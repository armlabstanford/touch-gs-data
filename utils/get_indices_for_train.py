import argparse
import os
import math
from typing import List, Tuple

import numpy as np



def get_train_eval_split_fraction(image_filenames: List, train_split_fraction: float) -> Tuple[np.ndarray, np.ndarray]:
    """
    Get the train/eval split fraction based on the number of images and the train split fraction.

    Args:
        image_filenames: list of image filenames
        train_split_fraction: fraction of images to use for training
    """

    # filter image_filenames and poses based on train/eval split percentage
    num_images = len(image_filenames)
    num_train_images = math.ceil(num_images * train_split_fraction)
    num_eval_images = num_images - num_train_images
    i_all = np.arange(num_images)
    i_train = np.linspace(
        0, num_images - 1, num_train_images+1, dtype=int
    )  # equally spaced training images starting and ending at 0 and num_images-1
    # remove last value from i_train
    i_train = i_train[:-1]
    i_eval = np.setdiff1d(i_all, i_train)  # eval images are the remaining images
    assert len(i_eval) == num_eval_images
    
    print("Train images indices: ", i_train)

    return i_train, i_eval


def get_all_images(base_path, images_path):
    """
    Get all images based on the list of image filenames.

    Args:
        image_filenames: list of image filenames
    """
    
    image_filenames = os.listdir(os.path.join(base_path, images_path))
    
    print(image_filenames)
    
    return image_filenames



if __name__ == "__main__":
    # get list of image filenames
    parser = argparse.ArgumentParser(description='Get indices ')
    
    parser.add_argument('--root_dir', type=str, required=True, help='Root dir.')
    parser.add_argument('--image_dir', type=str, required=True, help='Directory for images.')
    
    
    args = parser.parse_args()
    
    
    
    image_filenames = ['image1.png', 'image2.png', 'image3.png', 'image4.png', 'image5.png']
    train_split_fraction = 0.13
    get_train_eval_split_fraction(image_filenames, train_split_fraction)