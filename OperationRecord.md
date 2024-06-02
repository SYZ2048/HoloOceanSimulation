# Operation Record

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



### Issue

##### 水体环境设置

https://github.com/byu-holoocean/HoloOcean/issues/25

Q：光学照相机可以工作但是声纳不行

A：碰撞相关的问题

waterbodylake设置为如下时可以运行，如果选择generate collisions就会报错

<img src="C:\Users\xinruiy\AppData\Roaming\Typora\typora-user-images\image-20240521195252436.png" alt="image-20240521195252436" style="zoom: 33%;" />

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