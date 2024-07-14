import trimesh

path_to_baseline_model = r'./ExampleLevel_staticmesh.ply'
path_to_nerf_model = r'./00300228_Mesh_DenoiseManual.ply'


# 读取两个网格
mesh1 = trimesh.load(path_to_baseline_model)
mesh2 = trimesh.load(path_to_nerf_model)

# 计算Hausdorff距离
distance = mesh1.hausdorff_distance(mesh2)
print("Hausdorff Distance:", distance)