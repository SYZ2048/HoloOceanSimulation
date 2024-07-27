#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：HoloTest 
@File    ：get_viewpoint.py
@IDE     ：PyCharm 
@Author  ：SYZ
@Date    ：2024/5/5 19:30
To obtain viewpoints in Neusis dataset
"""
import os
import matplotlib.pyplot as plt
import numpy as np
from holoocean.tools.pklOperation import load_single_pkl


'''data keys: 
OrientationSensor (3, 3)
LocationSensor (3,)
PoseSensor (4, 4)
VelocitySensor (3,)
IMUSensor (4, 3)
DVLSensor (7,)
DepthSensor (1,)
ImagingSonar (512, 96)
t: float
'''


if __name__ == '__main__':
    # 提供 `.pkl` 文件的路径C:\Users\xinruiy\Python_code\holoocean\neusis_data\14deg_planeFull\Data
    pickle_loc = "./neusis_data/14deg_planeFull/Data/"

    camera_positions =[]
    camera_directions = []

    # 检查路径是否存在
    for pkls in os.listdir(pickle_loc):
        file_path = os.path.join(pickle_loc, pkls)
        data = load_single_pkl(file_path)
        camera_positions.append(data['LocationSensor'])
        camera_directions.append(data['OrientationSensor'])
    camera_positions = np.array(camera_positions)

    # 创建3D绘图
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # 绘制拍摄位置
    ax.scatter(camera_positions[:, 0], camera_positions[:, 1], camera_positions[:, 2], c='r', marker='o',
               label='Camera Positions')

    # 绘制方向向量
    first = True
    for position, orientation in zip(camera_positions, camera_directions):
        # 使用方向矩阵的第一列向量作为相机前向向量
        forward_vector = orientation[:, 0]
        if first:
            ax.quiver(position[0], position[1], position[2], forward_vector[0], forward_vector[1], forward_vector[2],
                      length=1.0, color='b', label='Camera Direction', linewidth=2)
            first = False
        else:
            ax.quiver(position[0], position[1], position[2], forward_vector[0], forward_vector[1], forward_vector[2],
                      length=1.0, color='b', linewidth=2)

    # 设置标签
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()

    # 显示绘图
    plt.show()
