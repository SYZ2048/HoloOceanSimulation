#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：HoloTest 
@File    ：SonarDisplayRealtime.py
@IDE     ：PyCharm 
@Author  ：SYZ
@Date    ：2024/5/7 20:48 
"""

import numpy as np
import matplotlib.pyplot as plt


class SonarDisplay:
    def __init__(self, azi, minR, maxR, binsR, binsA):
        plt.ion()  # 交互模式
        self.fig, self.ax = plt.subplots(subplot_kw=dict(projection='polar'), figsize=(8, 5))
        self.ax.set_theta_zero_location("N")
        self.ax.set_thetamin(-azi / 2)
        self.ax.set_thetamax(azi / 2)

        theta = np.linspace(-azi / 2, azi / 2, binsA) * np.pi / 180
        r = np.linspace(minR, maxR, binsR)
        T, R = np.meshgrid(theta, r)
        z = np.zeros_like(T)

        self.plot = self.ax.pcolormesh(T, R, z, cmap='gray', shading='auto', vmin=0, vmax=1)
        plt.tight_layout()

    def update_display(self, data):
        self.plot.set_array(data.ravel())
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def close_display(self):
        plt.ioff()
        plt.close(self.fig)
