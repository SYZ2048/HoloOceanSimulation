import holoocean
import matplotlib.pyplot as plt
import numpy as np

from KeyboardControl import start_keyboard_listener, parse_keys, pressed_keys

#### GET SONAR CONFIG
scenario = "Dam-HoveringImagingSonar"   # OpenWater-HoveringImagingSonar, PierHarbor-HoveringImagingSonar
config = holoocean.packagemanager.get_scenario(scenario)
config = config['agents'][0]['sensors'][-1]["configuration"]
azi = config['Azimuth']
minR = config['RangeMin']
maxR = config['RangeMax']
binsR = config['RangeBins']
binsA = config['AzimuthBins']

#### GET PLOT READY
plt.ion()
fig, ax = plt.subplots(subplot_kw=dict(projection='polar'), figsize=(8, 5))
ax.set_theta_zero_location("N")
ax.set_thetamin(-azi / 2)
ax.set_thetamax(azi / 2)

theta = np.linspace(-azi / 2, azi / 2, binsA) * np.pi / 180
r = np.linspace(minR, maxR, binsR)
T, R = np.meshgrid(theta, r)
z = np.zeros_like(T)

plt.grid(False)
plot = ax.pcolormesh(T, R, z, cmap='gray', shading='auto', vmin=0, vmax=1)
plt.tight_layout()
fig.canvas.draw()
fig.canvas.flush_events()

#### 初始化键盘监听
force = 25
keyboard_listener = start_keyboard_listener()

#### RUN SIMULATION
# command = np.array([0,0,0,0,20,20,20,20])
with holoocean.make(scenario) as env:
    while True:
        if 'q' in pressed_keys:
            break

        # 更新控制命令
        command = parse_keys(pressed_keys, force)
        env.act('auv0', command)

        # 刷新环境状态
        state = env.tick()

        if 'ImagingSonar' in state:
            s = state['ImagingSonar']
            plot.set_array(s.ravel())

            fig.canvas.draw()
            fig.canvas.flush_events()

print("Finished Simulation!")
plt.ioff()
plt.close(fig)
keyboard_listener.stop()
# 关闭所有绘图窗口
