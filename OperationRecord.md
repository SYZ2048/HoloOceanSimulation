# Nerf-Sonar Operation Record

### To do

#### 找到一个量化的指标评估重建性能，论文中用的root mean square (RMS) and mean Hausdorff distance errors (all in meters)



**mesh对比**：



Nerf——放大十倍——旋转到平行——移动

<img src=".\Images_Markdown\image-20240716102909256.png" alt="image-20240716102909256" style="zoom:25%;" />

用meshlab比对mesh：手动进行了Align然后做比对，Align参照[Aligning Models in Meshlab (youtube.com)](https://www.youtube.com/watch?v=30bJcj6yA4c)，比对参照[Comparing Meshes in Meshlab (youtube.com)](https://www.youtube.com/watch?v=O_3O_BuPkyA)

结果

```
Hausdorff Distance computed

Sampled 3250 pts (rng: 0) on ExampleLevel_staticmesh.ply searched closest on 00300228_Mesh_DenoiseManual_10.ply

min : 0.017456 max 544.781006 mean : 62.335575 RMS : 85.735085

Values w.r.t. BBox Diag (9949.872070)

min : 0.000002 max 0.054753 mean : 0.006265 RMS : 0.008617 

Applied filter Hausdorff Distance in 56 msec
```



#### baseline效果改进

**增加视角**：在之前建模中错误建模的地方总计增加了100个新的采样点——无法得到任何可靠重建

**训练cfg修改**：

#### 做稀疏视角的网络



### Train 

参照[rpl-cmu/neusis: Release code for Neural Implicit Surface Reconstruction using Imaging Sonar (ICRA 2023) (github.com)](https://github.com/rpl-cmu/neusis)

##### conf文件 

完整版见[HoloOceanSimulation/train_cfg/plane_vertical_raw.conf at master · SYZ2048/HoloOceanSimulation (github.com)](https://github.com/SYZ2048/HoloOceanSimulation/blob/master/train_cfg/plane_vertical_raw.conf)

```
mesh { 
    object_bbox_min = [-15, -6, -45]  
    object_bbox_max = [15, 6, -25]
    x_max = 15,
    x_min = -15,
    y_max = 6,
    y_min = -6,
    z_max = -25,
    z_min = -45,
    level_set = 0
}
```



##### 训练命令

```
source ~/miniconda3/etc/profile.d/conda.sh
conda activate neusis
cd ~/neusis

# 添加数据集
cp /root/autodl-fs/plane_vertical_raw.zip ~/neusis/data
cd data
unzip xxx.zip

# 在neusis/conf下添加新的conf

cd ~/neusis
python run_sdf.py --conf confs/plane_vertical_raw.conf > view.log
```



##### 结果位置

800view: b97811803c-f1e4a99a



库安装

```
pip install numpy==1.19.5 -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
```









```
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
```

```
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
pip install torch==1.10.0+cu113 torchvision==0.11.0+cu113 torchaudio==0.10.0 -f https://download.pytorch.org/whl/torch_stable.html
print(torch.__version__)
print(torch.cuda.is_available())

python run_sdf.py --conf confs/<dataset_name>.conf
python run_sdf.py --conf confs/plane_vertical_raw.conf
```



##### 解压pak

```
"C:\Program Files\Epic Games\UE_4.27\Engine\Binaries\Win64\UnrealPak.exe" C:\Users\xinruiy\AppData\Local\holoocean\0.5.8\worlds\Windows\WindowsNoEditor\Holodeck\Content\Paks\Holodeck-WindowsNoEditor.pak -Extract C:\Users\xinruiy\Python_code\holoocean\engine\pak_content
```



##### create environment:

https://holoocean.readthedocs.io/en/master/develop/develop.html

##### 先关UE4再停脚本

##### Collision Complexity设置

setting the “Collision Complexity” option in the details section of the static mesh editor to “use complex collision as simple”.

预生成Octree

###  step：

修改environment：不要用water plugin

删除C:\Users\xinruiy\Python_code\holoocean\engine\Octrees\ExampleLevel下的Octrees

先play UE4，再run python脚本

先关UE4，再停脚本



### 飞机素材库

Commercial Long-Range Aircraft

飞机参数![img](.\images_Markdown\f97f480474fe8fd90a9feff45886e407.png)



### 数据采集

##### 竖着的飞机

左机翼[9.7, -2.5,  -37]

右机翼[-9.7, -2.5,  -37]

机头[-0.7 -1.2 -30]

机尾[-1.2 -2.5,  -52]

##### ~~自动化采集的数据~~（效果不好，已弃用）

```
                                                    90度
                                                    |
                                            180 ————|————
                                                    |
                                                    |
【0-300】
飞机背部：机尾到机头
"location": [-1.2, -7, -48], 
"rotation": [0.0, 0.0, 80.0]	
【300-600】
飞机背部：机尾到机头
"location": [1.2, -7, -48],		
"rotation": [0.0, 0.0, 105.0]
【600-900】
飞机背部：机尾到机头
"location": [0.3, -7, -48],		
"rotation": [0.0, 0.0, 90.0]
【900-1400】
右机翼到左机翼
"location": [9.7, -7,  -40],
"rotation": [0.0, 0.0, 90.0]
【会crush】
右机翼到左机翼
"location": [9.460258, 4.810762, -33.422295],
"rotation": [0.0, 0.0, 270.0]
【1400-1600 1600-1800】
机腹到两翼
"location": [0.3, 4.8, -36],
"rotation": [0.0, 0.0, 270.0]
【1800-2100]
飞机腹部：机尾到机头
"location": [-0.8, 4.8, -48], 
"rotation": [0.0, 0.0, 285.0]	
【2100-2400]
飞机腹部：机尾到机头
"location": [0.8, 4.5, -48],
"rotation": [0.0, 0.0, 260.0]	
【2400-2800】
机尾横扫
"location": [0.3, 4.5, -28],
"rotation": [0.0, 0.0, 270.0]

```



##### ~~平着的飞机~~

机头到机尾倒着向上走，机头左侧是x=3(200-500)，机头右侧是x=0(0-200)

```
            "location": [3, 0, -37],
            "rotation": [0.0, 0.0, 270.0]
            
command = [0.1, 0.1, 0.1, 0.1, -1, -1, -1, -1]
```

左侧机翼到右侧机翼500-1200

```
            "location": [13, 3, -37],
            "rotation": [0.0, 0.0, 180.0]
手动控制
```

~

### Issue

##### 在use complex collision as simple设置下，teapot和cube有半个表面无法成像

设置double sided geometry



##### 水体环境设置

https://github.com/byu-holoocean/HoloOcean/issues/25

Q：光学照相机可以工作但是声纳不行

A：碰撞相关的问题

waterbodylake设置为如下时可以运行，如果选择generate collisions就会报错

<img src=".\Images_Markdown\image-20240521195252436.png" alt="image-20240521195252436" style="zoom: 33%;" />

##### 物体的碰撞设置

https://github.com/byu-holoocean/HoloOcean/issues/51

custom环境更新后需要删除生成的Octrees

Dell上的位置为C:\Users\xinruiy\Python_code\holoocean\engine\Octrees\ExampleLevel

物体的设置如下图

![3828036875-CollisionSettings](https://private-user-images.githubusercontent.com/91915043/328316472-13c626a8-c62b-4abd-bc97-6c4562e49140.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MTYyOTE0NzAsIm5iZiI6MTcxNjI5MTE3MCwicGF0aCI6Ii85MTkxNTA0My8zMjgzMTY0NzItMTNjNjI2YTgtYzYyYi00YWJkLWJjOTctNmM0NTYyZTQ5MTQwLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDA1MjElMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwNTIxVDExMzI1MFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTFkNTA4NDU3YWQ2NDkyZDY4ODIwMzljNzljOTIyY2JiYjgzZjhkYzFlY2JjOTgzZmM0MTk0YTMwZTVmMjk1MjgmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.6TPIQZVA44typDVtSxVtTAbdA9aAr0BxIVDrd08RWSY)



##### 物体的collision mesh设置

https://github.com/byu-holoocean/HoloOcean/issues/29

collision mesh可能比物体本身的建模粗糙的多，所以需要设置Collision Complexity为 “use complex collision as simple”.



##### 声纳图像不成像

https://github.com/byu-holoocean/HoloOcean/issues/33

如果capacity不足，可以预先生成octreehttps://holoocean.readthedocs.io/en/master/usage/octree.html#octree-generation



##### 显存碎片化

但是会影响性能

    torch.cuda.empty_cache() 
    os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:512"


plane_vertical_raw.conf

```
conf {
    dataset =  plane_vertical_raw
    image_setkeyname = "images" 
    expID =   plane_vertical_raw
    timef = False
    filter_th = 0
    use_manual_bound = True
}


train {
    learning_rate = 5e-4
    learning_rate_alpha = 0.01 
    end_iter = 300000
    start_iter = 0 

    warm_up_end = 5000 
    anneal_end = 50000 
    select_valid_px = False

    save_freq = 10
    val_mesh_freq = 10
    report_freq = 1

    igr_weight = 0.1
    variation_reg_weight = 0

    arc_n_samples = 10 
    select_px_method = "bypercent" 
    num_select_pixels = 100
    px_sample_min_weight = 0.001
    randomize_points = True
    percent_select_true = 0.4
    r_div = False 
}


mesh { 
    object_bbox_min = [-15, -6, -45]  
    object_bbox_max = [11, 3, 0]
    x_max = 11,
    x_min = -15,
    y_max = 3,
    y_min = -6,
    z_max = 0,
    z_min = -45,
    level_set = 0
}

model {
    sdf_network {
        d_out = 65
        d_in = 3
        d_hidden = 64
        n_layers = 4
        skip_in = [2]
        multires = 6
        bias = 1
        scale = 1.0
        geometric_init = False
        weight_norm = True
    }

    variance_network {
        init_val = 0.3
    }

    rendering_network {
        d_feature = 64
        mode = idr
        d_in = 9
        d_out = 1
        d_hidden = 64
        n_layers = 4
        weight_norm = True
        multires_view = 4
        squeeze_out = True
    }

    neus_renderer {
        n_samples = 64 
        n_importance = 0 
        n_outside = 0 
        up_sample_steps = 4    
        perturb = 0
    }
}

```



## 一些尝试：

### 点云比对or mesh比对？

**点云**：Ground Truth (mesh)【UE4】 --> 导出为mesh【UE4】--> Ground Truth (point cloud) 【CloudCompare】

Nerf (point cloud) 

需要相同的点云数量和点云对应：但是UE4导出的点云分布非常不均匀，平面上几乎没有点云，用CloudCompare生成密集点云
