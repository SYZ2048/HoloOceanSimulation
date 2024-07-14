import open3d as o3d
import numpy as np
from scipy.spatial import KDTree

def read_point_cloud(file_path):
    pcd = o3d.io.read_point_cloud(file_path)
    return np.asarray(pcd.points)

def convert_coordinates(points, factor):
    return points * factor

def downsample_point_cloud(points, target_num_points):
    # 均匀下采样
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    num_points = len(points)
    if num_points > 2 * target_num_points:
        step_size = int(num_points / target_num_points)
        downsampled_pcd = pcd.uniform_down_sample(step_size)
        downsampled_points = np.asarray(downsampled_pcd.points)
    else:
        downsampled_points = points

    # 随机下采样
    if len(downsampled_points) > target_num_points:
        indices = np.random.choice(len(downsampled_points), target_num_points, replace=False)
        downsampled_points = downsampled_points[indices]

    return downsampled_points

def compute_rms_error(points1, points2):
    if len(points1) != len(points2):
        raise ValueError("Point clouds must have the same number of points")

    differences = points1 - points2
    squared_differences = np.square(differences)
    mean_squared_error = np.mean(squared_differences)
    rms_error = np.sqrt(mean_squared_error)
    return rms_error


def compute_mean_hausdorff_distance(points1, points2):
    tree1 = KDTree(points1)
    tree2 = KDTree(points2)

    distances1, _ = tree1.query(points2)
    distances2, _ = tree2.query(points1)

    mean_distance1 = np.mean(distances1)
    mean_distance2 = np.mean(distances2)

    mean_hausdorff_distance = max(mean_distance1, mean_distance2)
    return mean_hausdorff_distance


def compute_centroid(points):
    return np.mean(points, axis=0)


def initial_alignment(source_points, target_points):
    source_centroid = compute_centroid(source_points)
    target_centroid = compute_centroid(target_points)

    translation = target_centroid - source_centroid
    aligned_points = source_points + translation

    return aligned_points, translation


def align_point_clouds(source_points, target_points):
    source_pcd = o3d.geometry.PointCloud()
    source_pcd.points = o3d.utility.Vector3dVector(source_points)
    target_pcd = o3d.geometry.PointCloud()
    target_pcd.points = o3d.utility.Vector3dVector(target_points)

    threshold = 0.05  # 设置配准的阈值
    trans_init = np.identity(4)  # 初始变换矩阵

    # 使用ICP算法进行配准
    reg_p2p = o3d.pipelines.registration.registration_icp(
        source_pcd, target_pcd, threshold, trans_init,
        o3d.pipelines.registration.TransformationEstimationPointToPoint(),
        o3d.pipelines.registration.ICPConvergenceCriteria(max_iteration=2000))

    aligned_points = np.asarray(source_pcd.transform(reg_p2p.transformation).points)
    return aligned_points, reg_p2p.transformation

# source: Red       target: Green      aligned: Blue
def visualize_point_clouds(source_points, target_points, aligned_points):
    # source_pcd = o3d.geometry.PointCloud()
    # source_pcd.points = o3d.utility.Vector3dVector(source_points)
    # source_pcd.paint_uniform_color([1, 0, 0])  # Red

    target_pcd = o3d.geometry.PointCloud()
    target_pcd.points = o3d.utility.Vector3dVector(target_points)
    target_pcd.paint_uniform_color([0, 1, 0])  # Green

    aligned_pcd = o3d.geometry.PointCloud()
    aligned_pcd.points = o3d.utility.Vector3dVector(aligned_points)
    aligned_pcd.paint_uniform_color([0, 0, 1])  # Blue

    # o3d.visualization.draw_geometries([source_pcd, target_pcd, aligned_pcd])
    o3d.visualization.draw_geometries([target_pcd, aligned_pcd])

def apply_rotation(points, rotation_matrix):
    return np.dot(points, rotation_matrix.T)