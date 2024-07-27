import holoocean
import matplotlib.pyplot as plt
import numpy as np

from tools.KeyboardControl import start_keyboard_listener, parse_keys, pressed_keys
from tools.SonarDisplayRealtime import SonarDisplay

#### GET SONAR CONFIG
scenario = "OpenWater-HoveringImagingSonar"   # Dam-HoveringImagingSonar, OpenWater-HoveringImagingSonar, PierHarbor-HoveringImagingSonar
config = holoocean.packagemanager.get_scenario(scenario)
config = config['agents'][0]['sensors'][-1]["configuration"]


azi = config['Azimuth']
minR = config['RangeMin']
maxR = config['RangeMax']
binsR = config['RangeBins']
binsA = config['AzimuthBins']

#### GET PLOT READY
display = SonarDisplay(azi, minR, maxR, binsR, binsA)

#### 初始化键盘监听
force = 25
keyboard_listener = start_keyboard_listener()

#### RUN SIMULATION
# command = np.array([0,0,0,0,20,20,20,20])
# with holoocean.make(scenario) as env:   # scenario_cfg=config
with holoocean.make(scenario) as env:  # scenario_cfg=config
    while True:
        if 'q' in pressed_keys:
            break

        # 更新控制命令
        command = parse_keys(pressed_keys, force)
        env.act('auv0', command)

        # 刷新环境状态
        state = env.tick()
        # print(state["LocationSensor"][0:3])
        # for key in state:
        #     print(key)
        # if 'LocationSensor' in state:
        #     p = state["LocationSensor"][0:3]
        #     print("position: ", p)

        if 'ImagingSonar' in state:
            s = state['ImagingSonar']
            # print(s.shape)
            display.update_display(s)  # 更新显示

print("Finished Simulation!")
display.close_display()  # 关闭显示
keyboard_listener.stop()
# 关闭所有绘图窗口
