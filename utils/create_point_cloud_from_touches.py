# Stanford University, ARMLab 2023
# Touch-GS

import os
import random
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import numpy as np
import cv2
import open3d as o3d

import colmap_utils_transforms


def get_point_cloud_from_depth_and_color(depth_image, color_image, camera_intrinsics, camera_extrinsics, scaling_factor=1):
    """
    gets the point cloud from the depth and color images
    
    Args:

    depth_image (np.array): The depth image.
    color_image (np.array): The color image.
    camera_intrinsics (list): The camera intrinsics.
    camera_extrinsics (np.array): The camera extrinsics.
    scaling_factor (float): The scaling factor for the depth image.
    
    Returns:
    
    points (np.array): The 3D points.
    """
    fx = camera_intrinsics[0]
    fy = camera_intrinsics[1]
    
    cx = camera_intrinsics[2]
    cy = camera_intrinsics[3]
    
    R = camera_extrinsics[:3, :3]
    t = camera_extrinsics[:3, 3]
    
    # Prepare the 3D point cloud by backprojecting the depth image
    points = []
    colors = []
    
    for v in range(depth_image.shape[0]):
        for u in range(depth_image.shape[1]):
            if depth_image[v, u] == 0: 
                continue  # Skip no depth
            color = color_image[v, u]
            Z = depth_image[v, u] / scaling_factor  # Assume a scaling factor if the depth is not in meters
            if Z == 0: continue  # Skip no depth
            X = (u - cx) * Z / fx
            Y = (v - cy) * Z / fy
            points.append([X, Y, Z])
            colors.append(color)
            
    # Transform points to world coordinates
    
    t = np.array([[t[0]], [t[1]], [t[2]]])  # Example translation vector
    
    R = R @ np.array([[1, 0, 0], [0, -1, 0], [0, 0, -1]])  # Example rotation matrix
    
    points_world = np.dot(R, np.transpose(points)) + t
    points_world = np.transpose(points_world)
    
    points = np.array(points_world)
    colors = np.array(colors)
    colors_normalized = colors / 255.0

    return points, colors_normalized    


def matplot_3d_point_cloud(points, colors):
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Scatter plot
    ax.scatter(points[:, 0], points[:, 1], points[:, 2], s=1, c=colors, marker='.')

    # Set axes labels
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Optionally set equal aspect ratio
    max_range = np.array([points[:, 0].max()-points[:, 0].min(), points[:, 1].max()-points[:, 1].min(), points[:, 2].max()-points[:, 2].min()]).max() / 2.0
    mid_x = (points[:, 0].max()+points[:, 0].min()) * 0.5
    mid_y = (points[:, 1].max()+points[:, 1].min()) * 0.5
    mid_z = (points[:, 2].max()+points[:, 2].min()) * 0.5
    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)

    # Show the plot
    plt.show()
    
def open3d_point_cloud(points, colors):
    pcd = o3d.geometry.PointCloud()

    # Assign the points to the point cloud
    pcd.points = o3d.utility.Vector3dVector(points)

    # Assign the colors to the point cloud
    pcd.colors = o3d.utility.Vector3dVector(colors)

    # Visualize the point cloud
    o3d.visualization.draw_geometries([pcd])


def get_all_point_clouds(image_dir, touch_depth_dir, colmap_camera_transformations, camera_intrinsics):
    image_filenames  = sorted(os.listdir(image_dir))
    depth_filenames = sorted(os.listdir(touch_depth_dir))
    
    limited_points_xyz = None
    limited_points_rgb = None
    
    i_take = list(range(len(image_filenames)))
    
    # get images we want
    # i_take = [0, 12, 24, 37, 49, 61, 74, 86]  # 8 image case
    
    # i_take = [0, 1, 2, 4, 5, 6, 8, 9, 11, 12, 13, 15, 16, 18, 19, 20, 22, 23, 25, 26, 27, 29, 30, 32,
    #                33, 34, 36, 37, 38, 40, 41, 43, 44, 45, 47, 48, 50, 51, 52, 54, 55, 57, 58, 59, 61, 62, 64, 65,
    #                66, 68, 69]
    
    # get the image indices for training
    
    i_take = [0, 1, 2, 3, 4, 6, 7, 8, 9, 11, 12, 13, 14, 15, 17, 18, 19, 20, 22, 23, 24, 25, 26, 28, 29, 30, 31, 33, 34, 35, 36, 37, 39, 40, 41, 42, 44, 45, 46, 47, 48, 50, 51, 52, 53, 55, 56, 57, 58, 59, 61, 62, 63, 64, 66, 67, 68, 69]
    
    
    for i in range(len(image_filenames)):
        image_filename = image_filenames[i]
        depth_filename = depth_filenames[i]
        var_dir = 'touch_var'
        
        var = cv2.imread(f'{var_dir}/{depth_filename}', cv2.IMREAD_ANYDEPTH) / 1000
        
        # filter out depths that are too far away
        if i in i_take:
            # plt.imshow(depth, cmap='viridis')
            # plt.colorbar()  
            # plt.show()
            image = cv2.imread(f'{image_dir}/{image_filename}')
            depth = cv2.imread(f'{touch_depth_dir}/{depth_filename}', cv2.IMREAD_ANYDEPTH) / 1000
            var = cv2.imread(f'{var_dir}/{depth_filename}', cv2.IMREAD_ANYDEPTH) / 1000
            # depth[depth > 2] = 0
            # take depths with var less than 0.6
            depth[var > 0.7] = 0
        
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            camera_extrinsics = colmap_camera_transformations[image_filename.split('.')[0]]
            
            image = cv2.imread(f'{image_dir}/{image_filename}')
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            points, colors = get_point_cloud_from_depth_and_color(depth, image, camera_intrinsics, camera_extrinsics)
            if limited_points_xyz is None:
                limited_points_xyz = points
                limited_points_rgb = colors
            else:
                limited_points_xyz = np.concatenate((limited_points_xyz, points))
                limited_points_rgb = np.concatenate((limited_points_rgb, colors))
            print('Got point cloud for', image_filename)
            
            
    # take a small fraction of the points
    # limited_points_xyz = limited_points_xyz[::100]
    # limited_points_rgb = limited_points_rgb[::100]

    # percentage = 20

    # # Calculate the number of points to select
    # num_to_select = int(len(points) * (percentage / 100))

    # # Use random.sample to randomly select points
    # selected_points = random.sample(points, num_to_select)
    
    percentage = 5
    
    total_indices = len(limited_points_xyz)
    num_indices_to_select = int(total_indices * (percentage / 100))

    # Generate a list of all indices
    all_indices = list(range(total_indices))

    # Use random.sample to randomly select indices
    selected_indices = random.sample(all_indices, num_indices_to_select)
    
    limited_points_rgb = limited_points_rgb[selected_indices]
    limited_points_xyz = limited_points_xyz[selected_indices]

    open3d_point_cloud(limited_points_xyz, limited_points_rgb)
    return limited_points_xyz, limited_points_rgb * 255.0
    
    
    
if __name__ == '__main__':
    transforms = colmap_utils_transforms.read_nerfstudio_transform_positions('transforms.json', return_full_transforms=True)
    
    # transforms = colmap_utils_transforms.read_blender_transform_positions('transforms_train_full.json', return_full_transforms=True)
    fx = 1297
    fy = 1304
    
    cx = 620.91
    cy = 238.28
    
    camera_instrinsics = [fx, fy, cx, cy]
    
    points, colors = get_all_point_clouds(image_dir='train', touch_depth_dir='touch_depth', colmap_camera_transformations=transforms, camera_intrinsics=camera_instrinsics)
    
    # save points and colors to .npy files
    np.save('points_bunny.npy', points)
    np.save('colors_bunny.npy', colors)