import open3d as o3d

# 文件路径
path_to_baseline_model = r'./ExampleLevel.ply'
path_to_nerf_model = r'../Result_syz/plane_vertical_raw_800/meshes/00300228.ply'
file_path = path_to_nerf_model

# 尝试读取点云
point_cloud = o3d.io.read_point_cloud(file_path)
# 尝试读取网格
triangle_mesh = o3d.io.read_triangle_mesh(file_path)

# 检查文件内容
if not triangle_mesh.is_empty():
    print("The file contains a triangle mesh.")
    print(triangle_mesh)
    o3d.visualization.draw_geometries([triangle_mesh])
elif not point_cloud.is_empty():
    print("The file contains a point cloud.")
    print(point_cloud)
    o3d.visualization.draw_geometries([point_cloud])
else:
    print("The file does not contain a recognizable point cloud or triangle mesh.")