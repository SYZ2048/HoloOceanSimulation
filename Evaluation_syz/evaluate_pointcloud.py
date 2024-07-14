"""
@Project ：HoloTest
@File    ：evaluate_pointcloud.py
@IDE     ：PyCharm
@Author  ：SYZ
Read *.ply file to evaluate
"""

import open3d as o3d
import numpy as np
from scipy.spatial import KDTree
from PointCloudEvaluate import *

def filter_points_by_z(points, z_threshold):
    return points[points[:, 2] <= z_threshold]

def adjust_z_coordinates(points, z_offset):
    points[:, 2] += z_offset
    return points




# 读取基准模型和NeRF重建模型的点云数据
path_to_baseline_model = r'./ExampleLevel_StaticMesh_PointCloud.ply'
path_to_nerf_model = r'./00300228_Pointcloud_DenoiseManual.ply'
baseline_points = read_point_cloud(path_to_baseline_model)
nerf_points = read_point_cloud(path_to_nerf_model)


# 过滤掉Z坐标大于-25的点
nerf_points = filter_points_by_z(nerf_points, -5)
# 将NeRF点云数据的单位转换（乘以100）
nerf_points = convert_coordinates(nerf_points, 300)
# 假设需要绕X轴旋转90度
rotation_matrix = np.array([
    [1, 0, 0],
    [0, 0, 1],
    [0, -1, 0]
])
nerf_points = apply_rotation(nerf_points, rotation_matrix)
# 调整NeRF点云的Z坐标，增加200
nerf_points = adjust_z_coordinates(nerf_points, -1000)

# 打印点云数量
print(f"Baseline points: {len(baseline_points)}")
print(f"NeRF points: {len(nerf_points)}")

# 确保两个点云数量一致
target_num_points = min(len(baseline_points), len(nerf_points))
baseline_points = downsample_point_cloud(baseline_points, target_num_points)
nerf_points = downsample_point_cloud(nerf_points, target_num_points)

# 初始对齐
initial_aligned_points, translation = initial_alignment(nerf_points, baseline_points)


# 对齐点云
aligned_nerf_points, transformation_matrix = align_point_clouds(nerf_points, baseline_points)
print("Transformation matrix:")
print(transformation_matrix)

# 打印对齐后的点云部分数据以检查对齐是否正确
print("Sample of aligned NeRF points:")
print(aligned_nerf_points[:5])
print("Sample of baseline points:")
print(baseline_points[:5])

# 可视化点云 source: Red       target: Green      aligned: Blue
visualize_point_clouds(nerf_points, baseline_points, aligned_nerf_points)




# 计算对齐后的RMS误差和Mean Hausdorff距离
rms_error = compute_rms_error(baseline_points, aligned_nerf_points)
mean_hausdorff_distance = compute_mean_hausdorff_distance(baseline_points, aligned_nerf_points)

print(f"Aligned RMS Error: {rms_error} meters")
print(f"Aligned Mean Hausdorff Distance: {mean_hausdorff_distance} meters")