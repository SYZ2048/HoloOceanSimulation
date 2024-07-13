#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：HoloTest 
@File    ：KeyboardControl.py
@IDE     ：PyCharm 
@Author  ：SYZ
@Date    ：2024/5/5 16:28 
"""
import numpy as np
from pynput import keyboard

# 初始化键盘监听器的按键列表
pressed_keys = list()

# 键盘按下事件的处理程序
def on_press(key):
    global pressed_keys
    if hasattr(key, 'char') and key.char not in pressed_keys:
        pressed_keys.append(key.char)

# 键盘释放事件的处理程序
def on_release(key):
    global pressed_keys
    if hasattr(key, 'char') and key.char in pressed_keys:
        pressed_keys.remove(key.char)

# 启动键盘监听器
def start_keyboard_listener():
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    return listener

# 解析按键输入并生成控制命令
def parse_keys(keys, val):
    command = np.zeros(8)
    val_x100 = val * 100
    if 'i' in keys:
        command[0:4] += val_x100
    if 'k' in keys:
        command[0:4] -= val_x100
    if 'j' in keys:
        command[[4,7]] += val
        command[[5,6]] -= val
    if 'l' in keys:
        command[[4,7]] -= val
        command[[5,6]] += val
    if 'w' in keys:
        command[4:8] += val_x100
    if 's' in keys:
        command[4:8] -= val_x100
    if 'a' in keys:
        command[[4,6]] += val_x100
        command[[5,7]] -= val_x100
    if 'd' in keys:
        command[[4,6]] -= val_x100
        command[[5,7]] += val_x100
    return command
