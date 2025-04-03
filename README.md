# CardiacField项目复现说明
## 原项目地址和下载
本仓库中的 ``CardiacField`` 文件夹已经对错误的源码进行修改，您可以选择下载原项目，如下所示：

[📥 直接下载原项目ZIP包](https://github.com/cshennju/CardiacField/archive/refs/heads/main.zip)

[🚀 点击此处打开原项目仓库](https://github.com/cshennju/CardiacField)

## 项目简述
对该项目的概括：**使用二维超声探头通过隐式神经表示（INR）网络重建三维心脏**

该项目在特殊而简单的心脏 2D B超图片采集的基础上，只需要不足 5min 便可实现心脏的三维重建。优势如下所述：

- 每个患者独立建模，无需预训练数据集
- 低成本高精度：仅需常规2D探头，实现接近3DE的EF准确性
- 简化操作流程（心尖环扫），适合非专科人员使用



## 环境配置
克隆项目 ``git clone https://github.com/cshennju/NeuralCMF.git``

anaconda配置下安装torch-scatter ``conda install pytorch-scatter -c pyg``，[其他安装环境](https://github.com/rusty1s/pytorch_scatter#installation)

安装tinycudann ``pip install git+https://github.com/NVlabs/tiny-cuda-nn/#subdirectory=bindings/torch``

安装apex
```
git clone https://github.com/NVIDIA/apex
cd apex
# if pip >= 23.1 (ref: https://pip.pypa.io/en/stable/news/#v23-1) which supports multiple `--config-settings` with the same key... 
pip install -v --disable-pip-version-check --no-cache-dir --no-build-isolation --config-settings "--build-option=--cpp_ext" --config-settings "--build-option=--cuda_ext" ./
# otherwise
pip install -v --disable-pip-version-check --no-cache-dir --no-build-isolation --global-option="--cpp_ext" --global-option="--cuda_ext" ./
```
> 注意，安装 apex 时间较长（大约30min）

安装成功以上插件之后，创建一个 conda 环境 ``conda create -name card``

执行 ``pip install -r requirements.txt`` 命令配置项目所需环境

## 数据集说明：心尖环扫
操作者只需围绕心尖旋转探头360°，采集多视角2D图像（约200帧）

系统自动筛选120帧高质量图像用于重建
-  高质量：结构清晰、噪声低、无运动伪影
-  空间覆盖均匀：探头旋转角度间隔均匀（理想间隔3°），覆盖心脏全视角
-  心脏周期同步：基于ECG信号选择舒张末期（ED）和收缩末期（ES）的关键相位

评价指标：
-  结构清晰度：通过图像梯度幅值（如Sobel算子）量化边缘锐利度
-  信噪比（SNR）：计算心肌区域与背景噪声的强度对比
-  心脏结构完整性：使用轻量级CNN检测关键解剖结构（如左心室腔、室间隔）的可见性


## 源码改动部分
### 源码错误修正

![alt text](image.png)

将 ``train_heart.py`` 第144行的代码修改为如上图所示

![alt text](image-1.png)
### 路径修改
#### vis_3D.py
生成 ``.mat`` 文件时，注意调用正确的路径，这这里已经将默认文件夹修改

![alt text](image-2.png)
#### mat2nii.py
将 ``.mat`` 文件转化为 ``.nii``格式文件时，也要注意路径的正确调用，此处也以修改

![alt text](image-3.png)
## 增加代码说明
为了方便在 Blender 中查看3D心脏的全局面貌，这里增加如下代码，将 ``.mat`` 文件转化为 ``.obj`` 文件，导入 Blender 中即可查看

```py
import scipy.io
import numpy as np
from skimage.measure import marching_cubes
import trimesh

# 加载.mat文件
data = scipy.io.loadmat('2d_example_3d.mat')
gray = data['gray']

# 生成等值面（假设阈值为0）
vertices, faces, normals, _ = marching_cubes(gray, level=0)

# 创建网格并导出为.obj
mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
mesh.export('output_2d3d.obj')
```

注意，在上述代码中，gray 是 ``.mat`` 文件中对应的非自动生成的键名，运行以下代码查看键名，就是对 gray 变量赋值的字符串

```py
import scipy.io

# 加载.mat文件
mat_data = scipy.io.loadmat('straus_3d.mat')

# 查看所有键（变量名）
print(mat_data.keys())

# 过滤掉MATLAB系统自动生成的键（如 __header__, __version__ 等）
keys = [key for key in mat_data.keys() if not key.startswith('__')]
print("用户定义的变量名:", keys)
```

## 项目执行流程说明
在配置好环境之后，依次执行下面的指令

激活 conda 环境

训练得到权重文件 ``python train_heart.py --root_dir './2d_example/' --exp_name '/2d_example/'`` ，ckpt 文件保存于 ckpts 文件夹中

执行 ``python vis_3D.py --root_dir '2d_example'`` 得到 ``.mat`` 文件

执行 ``python mat2nii.py`` 得到 ``.nii`` 文件，导入 3D Slicer 中查看，注意源代码中的文件路径调用

执行 ``seeKey.py`` 查看 ``.mat`` 的键名，注意源代码中的文件路径调用

执行 ``trans.py`` 将 ``.mat`` 文件变成 ``.obj``文件在 Blender 中查看，注意源代码中的文件路径调用

## 结果展示

``.mat`` ``.nii`` ``.obj`` 置于 ``实验结果文件`` 文件夹中

在 3D Slicer 中查看 ``.nii`` 文件

![alt text](image-4.png)

在 Blender 中查看 ``.obj`` 文件

![alt text](image-5.png)


