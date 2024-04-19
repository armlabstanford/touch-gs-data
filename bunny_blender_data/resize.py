import json
import os


from PIL import Image

KEY_TO_PATH = {
    'file_path': 'image',
    'depth_file_path': 'depth',
    'uncertainty_file_path': 'uncertainty'
}


def update_transforms_with_scale_factor(json_file_path, new_json_file_path, resized_dir_prefix='resized'):

    # Path to the JSON file
    # The scale factor by which to resize the images and update parameters
    scale_factor = 0.5  # Replace with the desired scale factor

    # Read the JSON file
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Update the parameters with the scale factor
    data['w'] = int(data['w'] * scale_factor)
    data['h'] = int(data['h'] * scale_factor)
    data['fl_x'] = data['fl_x'] * scale_factor
    data['fl_y'] = data['fl_y'] * scale_factor
    data['cx'] = data['cx'] * scale_factor
    data['cy'] = data['cy'] * scale_factor
    
    

    # Iterate over each frame and update the file paths
    for frame in data['frames']:
        for key in ['file_path', 'depth_file_path', 'uncertainty_file_path']:
            # Compute the new path by adding a suffix before the file extension
            original_path = frame[key]
            
            resized_dir_name = KEY_TO_PATH[key]
            
            full_resized_dir_name = f'{resized_dir_prefix}_{resized_dir_name}'
        
            os.makedirs(full_resized_dir_name, exist_ok=True)
            
            
            print(original_path)
            
            path_parts = original_path.split('.')
            path_parts[0] = os.path.join(full_resized_dir_name, os.path.basename(path_parts[0]))
            print(path_parts)
            new_path = f"{path_parts[0]}.{path_parts[1]}"
            
            print(new_path)
            
            frame[key] = new_path  # Update the path in the JSON data
            
            # # Resize and save the images
            with Image.open(original_path) as img:
                img_resized = img.resize((data['w'], data['h']))
                img_resized.save(new_path)


    # Save the updated JSON data to a new file
    with open(new_json_file_path, 'w') as file:
        json.dump(data, file, indent=4)

    print(f"The updated JSON data has been saved to {new_json_file_path}")


if __name__ == '__main__':
    update_transforms_with_scale_factor("transforms_old.json", "transforms.json")