#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：HoloTest 
@File    ：get_viewpoint.py
@IDE     ：PyCharm 
@Author  ：SYZ
@Date    ：2024/5/5 19:30 
"""
import pickle
import cv2
import os
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from pklOperation import load_single_pkl

# 提供 `.pkl` 文件的路径C:\Users\xinruiy\Python_code\holoocean\neusis_data\14deg_planeFull\Data
pickle_loc = "./neusis_data/14deg_planeFull/Data/"

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
    camera_positions =[]
    camera_directions = []
    # 检查路径是否存在
    for pkls in os.listdir(pickle_loc):
        file_path = os.path.join(pickle_loc, pkls)
        data = load_single_pkl(file_path)
        camera_positions.append(data['LocationSensor'])
    camera_positions =np.array(camera_positions)

    # 创建3D绘图
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # 绘制拍摄位置
    ax.scatter(camera_positions[:, 0], camera_positions[:, 1], camera_positions[:, 2], c='r', marker='o',
               label='Camera Positions')

    # 绘制方向向量
    # for position, direction in zip(camera_positions, camera_directions):
    #     ax.quiver(position[0], position[1], position[2], direction[0], direction[1], direction[2], length=0.5,
    #               normalize=True, color='b')

    # 设置标签
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()

    # 显示绘图
    plt.show()
