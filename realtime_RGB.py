#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：HoloOcean 
@File    ：realtime_RGB.py
@IDE     ：PyCharm 
@Author  ：SYZ
@Date    ：2024/4/28 16:57 
"""
import holoocean
import cv2
from KeyboardControl import start_keyboard_listener, parse_keys, pressed_keys

# 初始化环境
env = holoocean.make("Dam-HoveringCamera")

# 初始化键盘监听器
force = 25
keyboard_listener = start_keyboard_listener()

# 主循环
cv2.namedWindow("Camera Output")
while True:
    if 'q' in pressed_keys:
        break

    # 更新控制命令
    command = parse_keys(pressed_keys, force)
    env.act('auv0', command)

    # 刷新环境状态
    state = env.tick()

    # 如果有图像数据，则显示
    if "LeftCamera" in state:
        pixels = state["LeftCamera"]
        cv2.imshow("Camera Output", pixels[:, :, 0:3])
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cv2.destroyAllWindows()
keyboard_listener.stop()
