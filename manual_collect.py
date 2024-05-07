#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：HoloTest 
@File    ：manual_collect.py
@IDE     ：PyCharm 
@Author  ：SYZ
@Date    ：2024/5/7 19:54 
"""
import holoocean
import matplotlib.pyplot as plt
import numpy as np

from KeyboardControl import start_keyboard_listener, parse_keys, pressed_keys
from SonarDisplayRealtime import SonarDisplay

# GET SONAR CONFIG
scenario = "Dam-HoveringImagingSonar"  # OpenWater-HoveringImagingSonar, PierHarbor-HoveringImagingSonar
config = holoocean.packagemanager.get_scenario(scenario)
config = config['agents'][0]['sensors'][-1]["configuration"]

azi = config['Azimuth']
minR = config['RangeMin']
maxR = config['RangeMax']
binsR = config['RangeBins']
binsA = config['AzimuthBins']

# GET PLOT READY
display = SonarDisplay(azi, minR, maxR, binsR, binsA)

# 初始化键盘监听
force = 25
keyboard_listener = start_keyboard_listener()

# waypoints
# start: [-185, 46.7, -25]
x_coord = -185
y_coord = 46.7
# 使用 numpy.linspace 创建 z 坐标，假设我们需要 6 个点
z_coords = np.linspace(-25, -3, num=50)
# 使用 numpy.tile 和 numpy.stack 结合固定的 x, y 和变化的 z
waypoints = np.stack((np.full(z_coords.shape, x_coord),
                      np.full(z_coords.shape, y_coord),
                      z_coords), axis=-1)
num_way_points = waypoints.shape[0]

idx = 0
# RUN SIMULATION

# with holoocean.make(scenario) as env:   # scenario_cfg=config
with holoocean.make(scenario) as env:  # scenario_cfg=config
    for l in waypoints:
        env.draw_point([l[0], l[1], l[2]], lifetime=0)
    print("Going to waypoint ", idx)

    while True:
        if 'q' in pressed_keys:
            break

        # 更新控制命令
        command = parse_keys(pressed_keys, force)
        env.act('auv0', command)

        # 刷新环境状态
        state = env.tick()
        p = state["LocationSensor"][0:3]
        # print("position: ", p)
        dist = np.linalg.norm(p - waypoints[idx])
        # print("distance: ", dist)

        if dist < 1e-1:
            idx = (idx + 1) % num_way_points
            print("Going to waypoint ", idx)

        if 'ImagingSonar' in state:
            s = state['ImagingSonar']
            display.update_display(s)  # 更新显示

print("Finished Simulation!")
display.close_display()  # 关闭显示
keyboard_listener.stop()
# 关闭所有绘图窗口
