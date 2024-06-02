from holoocean.environments import HoloOceanEnvironment
import matplotlib.pyplot as plt
import numpy as np
import holoocean
import cv2
import os
import shutil
import json

from KeyboardControl import start_keyboard_listener, parse_keys, pressed_keys
from SonarDisplayRealtime import SonarDisplay
from pklOperation import save_single_pkl

# remove Octrees
Octrees_path = r'.\engine\Octrees\ExampleLevel'

new_octree_flag = False

if new_octree_flag:
    # 确认父文件夹存在
    if os.path.exists(Octrees_path):
        # 遍历父文件夹内的所有项目
        for item in os.listdir(Octrees_path):
            item_path = os.path.join(Octrees_path, item)
            # 如果项目是文件夹，则删除
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
                print(f'Remove {item_path}')
    else:
        print(f'{Octrees_path} does not exist')
    print('remove old Octrees')


#### GET SONAR CONFIG
with open('Custom_Environment_Config.json', 'r') as json_file:
    config_scenario = json.load(json_file)


config = config_scenario['agents'][0]['sensors'][-1]["configuration"]
azi = config['Azimuth']
minR = config['RangeMin']
maxR = config['RangeMax']
binsR = config['RangeBins']
binsA = config['AzimuthBins']

#### GET PLOT READY
display = SonarDisplay(azi, minR, maxR, binsR, binsA)

#### 初始化键盘监听
force = 0.1
keyboard_listener = start_keyboard_listener()


#### RUN SIMULATION
idx = 0
with HoloOceanEnvironment(scenario=config_scenario, start_world=False) as env:  # scenario_cfg=config
    while True:
        command = parse_keys(pressed_keys, force)
        env.act('auv0', command)

        state = env.tick()
        # if 'LocationSensor' in state:
        #     print(state['LocationSensor'])

        if 'ImagingSonar' in state:
            s = state['ImagingSonar']
            # print(s.shape)
            display.update_display(s)  # 更新显示

        if 'c' in pressed_keys and 'ImagingSonar' in state:
            save_single_pkl(os.path.join('./collect_data/plane', f"{idx}.pkl"),state)


print("Finished Simulation!")
