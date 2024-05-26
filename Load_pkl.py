#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：HoloTest 
@File    ：Load_pkl.py
@IDE     ：PyCharm 
@Author  ：SYZ
@Date    ：2024/5/5 19:30 
"""
import pickle
import cv2
import os
import matplotlib.pyplot as plt

# 提供 `.pkl` 文件的路径
# pickle_loc = "./neusis_14deg_planeFull/Data"
# image_output_loc = "./neusis_14deg_planeFull/Image_14deg_planeFull/ExtractedImages"
# image_output_loc = "{}/ExtractedImages".format(dirpath)


def load_img(pickle_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for pkls in os.listdir(pickle_folder):
        # 使用 'rb' 模式打开文件（以二进制读模式）
        # assert i < 10
        filename = "{}/{}".format(pickle_folder, pkls)
        print(pkls)
        with open(filename, 'rb') as f:
            # 反序列化文件，恢复原始对象
            data = pickle.load(f)
            # 使用 OpenCV 保存提取的图像
            if "ImagingSonar" in data:
                image = data["ImagingSonar"]

                # 对图像数据进行必要的预处理
                s = image.shape
                image[image < 0.05] = 0  # 将小于阈值的像素设置为 0
                image[s[0] - 200:, :] = 0  # 清除最后 200 行

                # 构建图像输出文件路径
                image_filename = "{}/{}.png".format(output_folder, pkls.split('.')[0])

                # 使用 OpenCV 保存提取的图像，确保图像数据在 [0, 255] 范围
                cv2.imwrite(image_filename, image * 255)

                print(f"Image successfully saved to: {image_filename}")
            else:
                print("The 'ImagingSonar' key is not found in the provided .pkl file.")


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


def load_single_pkl(file_path):
    # file_path = "./neusis_14deg_planeFull/Data/51.pkl"
    with open(file_path, 'rb') as file:
        # 反序列化文件，恢复原始对象
        data = pickle.load(file)
        # for key in data:
        #     # print(key)
        #     print(key, data[key].shape)
        return data


def save_single_pkl(output_path, object_to_save):
    # 将字典保存为 .pkl 文件
    with open(output_path, 'wb') as f:  # 'wb' 模式以二进制写入
        pickle.dump(object_to_save, f)
    # print(f"Dictionary has been successfully saved to {output_path}.")


if __name__ == '__main__':
    file_path = "D:/code_python/HoloTest/holoocean/pillar_14degree/Data"
    out_path = "D:/code_python/HoloTest/holoocean/pillar_14degree/Img_Sonar"
    # file_path = "D:/code_python/HoloTest/holoocean/neusis_14deg_planeFull/Data"
    # out_path = "D:/code_python/HoloTest/holoocean/neusis_14deg_planeFull/Image_14deg_planeFull/ExtractedImages"
    load_img(file_path, out_path)
# result = load_single_pkl(file_path)
# output_path = "./test.pkl"
# save_single_pkl(output_path, result)
# print(load_single_pkl(output_path))