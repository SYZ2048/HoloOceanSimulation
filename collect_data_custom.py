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
save_folder_path = 'collect_data/plane_vertical_raw/Data'
idx = 800

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
    print('remove old Octrees Done')

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
force = 0.05
keyboard_listener = start_keyboard_listener()

Sensor_key = ['OrientationSensor', 'LocationSensor', 'PoseSensor', 'VelocitySensor', 'IMUSensor', 'DVLSensor',
              'DepthSensor', 'ImagingSonar']



# for pkl_file in os.listdir(save_folder_path):
#     try:
#         os.remove(os.path.join(save_folder_path, pkl_file))
#     except Exception as e:
#         print(f"Cannot remove {pkl_file}: {e}")
# print("Remove old pkl files done")

#### RUN SIMULATION
with HoloOceanEnvironment(scenario=config_scenario, start_world=False) as env:  # scenario_cfg=config
    while True:
        command = parse_keys(pressed_keys, force)
        # command = [1, 1, 1, 1, 0, 0, 0, 0]
        # command = [0, 0, 0, 0, 0, 0, 0, 0]
        env.act('auv0', command)

        state = env.tick()
        # if 'LocationSensor' in state:
        #     print(state['LocationSensor'])

        if 'ImagingSonar' in state:
            s = state['ImagingSonar']
            # print(s.shape)
            display.update_display(s)  # 更新显示

        if 'q' in pressed_keys and all(item in state for item in Sensor_key):
            save_single_pkl(os.path.join(save_folder_path, f"{idx}.pkl"), state)
            idx += 1

print("Finished Simulation!")
