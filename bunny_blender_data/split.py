import random
import json
import numpy as np

CIRCLE_CENTER = np.array([2.6814, 2.545 , 0.96  ])

def split_transforms_data_randomly(data, train_percentage=80):
    """
    Splits the data into training and testing sets randomly based on the specified percentage.

    Args:
    - data: The original data to be split.
    - train_percentage: The percentage of data to be used for training.

    Returns:
    - train_data: The training subset of the data.
    - test_data: The testing subset of the data.
    """
    # Shuffling the frames randomly
    frames = data["frames"]
    random.shuffle(frames)
    
    total_frames = len(frames)
    train_size = int((train_percentage / 100.0) * total_frames)
    
    # Splitting the frames based on the calculated train size
    train_frames = frames[:train_size]
    test_frames = frames[train_size:]
    
    new_train_frames = []
    for frame in train_frames:
        T = np.array(frame["transform_matrix"])
        pos = T[:3, 3]
        new_pos = pos - CIRCLE_CENTER
        frame["transform_matrix"][0][3] = new_pos[0]
        frame["transform_matrix"][1][3] = new_pos[1]
        frame["transform_matrix"][2][3] = new_pos[2]
        
        new_train_frames.append(frame)
        
    new_test_frames = []
    for frame in test_frames:
        T = np.array(frame["transform_matrix"])
        pos = T[:3, 3]
        new_pos = pos - CIRCLE_CENTER
        frame["transform_matrix"][0][3] = new_pos[0]
        frame["transform_matrix"][1][3] = new_pos[1]
        frame["transform_matrix"][2][3] = new_pos[2]

        new_test_frames.append(frame)
    
    # Creating new data dictionaries for train and test splits
    train_data = {
        "camera_angle_x": data["camera_angle_x"],
        "frames": new_train_frames
    }
    
    test_data = {
        "camera_angle_x": data["camera_angle_x"],
        "frames": new_test_frames
    }
    
    return train_data, test_data

# Set seed for reproducibility
random.seed(42)

f = open('transforms_train_full.json')
json_data = json.load(f)

# Example usage with 70% of frames for training and 30% for testing
train_data_random, test_data_random = split_transforms_data_randomly(json_data, train_percentage=50)



# Saving the randomly split train and test data to JSON files
with open('transforms_train.json', 'w') as file:
    json.dump(train_data_random, file, indent=4)

with open('transforms_test.json', 'w') as file:
    json.dump(test_data_random, file, indent=4)

