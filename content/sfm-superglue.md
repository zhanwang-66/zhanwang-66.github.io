Title: SfM 三维重建：从 COLMAP 到 SuperGlue 特征匹配
Date: 2026-05-25 10:00
Category: 技术
Tags: SfM, SuperGlue, COLMAP, 特征匹配, 三维重建, LightGlue
Slug: sfm-superglue-feature-matching
Summary: 梳理 Structure from Motion（SfM）流程，从传统 COLMAP 方案到 SuperGlue / LightGlue 深度学习特征匹配，结合实验分析差异。

Structure from Motion（SfM）是计算机视觉中从多视角二维图像恢复三维结构与相机位姿的核心技术。本文梳理 SfM 完整流程，并聚焦特征匹配环节，对比传统方法与基于深度学习的 SuperGlue / LightGlue 方案。

## SfM 流程概览

SfM 基于多视图几何关系，从一组无序图像中同时估计相机参数与稀疏三维点云。典型流程：

> **输入图像 → 特征提取 → 特征匹配 → 几何验证 → 增量式稀疏重建 → Bundle Adjustment → 稀疏点云**

在此基础上可扩展：稠密点云（MVS）→ Mesh 建模 → 表面纹理 → 更前沿的 NeRF 或 3D Gaussian Splatting。

主流 SfM 工具包括 COLMAP（开源标杆）、VisualSFM、VVGT 等。

## COLMAP：经典流水线

COLMAP 是苏黎世联邦理工学院（ETH Zurich）开发的开源 SfM + MVS 流水线，提供图形界面与命令行接口，是学术研究与工业应用中最广泛使用的三维重建工具之一。其标准增量式 SfM 流程：

1. **特征提取** — 使用 Covariant SIFT 为每张图像提取局部特征点与描述子
2. **穷举匹配与几何验证** — 生成所有图像对，进行特征匹配并通过对极几何验证内点数
3. **增量式稀疏重建** — 选择初始图像对（高内点数 + 大基线）→ 逐张注册新图像（PnP 求解位姿）→ 三角化新增三维点 → 全局 Bundle Adjustment 优化重投影误差
4. **输出** — 相机内参/外参 + 稀疏三维点云

```
注册图像 #16 => 观察到 621 / 4393 个三维点
全局 Bundle Adjustment → 联合优化所有相机位姿与三维点位置
```

COLMAP 在纹理丰富的场景表现优秀，但其依赖 SIFT 特征在弱纹理、重复纹理、大视角变化下会出现大量误匹配，导致重建失败或精度下降。

## 深度学习特征匹配

传统特征匹配依赖手工规则（最近邻搜索 + 比值测试 + RANSAC 几何验证），在挑战性场景中鲁棒性不足。Magic Leap 团队提出的 SuperGlue 将深度学习引入匹配环节，显著提升了匹配质量。

### SuperPoint（特征提取）

SuperPoint（DeTone et al., CVPR 2018 Workshop）是自监督学习的特征点检测与描述子网络。在 Synthetic Shapes 数据集上预训练基础检测器，再通过单应性变换在真实图像上自举训练，无需人工标注。输出为每个像素点的兴趣分数与 256 维描述子。

### SuperGlue（特征匹配）

SuperGlue（Sarlin et al., CVPR 2020 **Oral**）是匹配两组局部特征的图神经网络。核心设计：

- **注意力图神经网络** — 在两组特征点内部和之间建立图结构，通过多头注意力聚合上下文信息，使网络能够联合推理三维场景结构与特征分配
- **可微分最优运输层** — 将匹配问题建模为最优运输问题，通过 Sinkhorn 算法迭代求解软分配矩阵。该层天然处理遮挡点与不可匹配点——为它们分配一个额外的 "dustbin" 通道
- **端到端训练** — 从图像对直接学习几何变换的先验知识，在室内外大基线场景的姿态估计上达到 state-of-the-art

SuperGlue 在现代 GPU 上可达到实时性能，可直接集成到现有 SfM 或 SLAM 系统中。代码与预训练权重在 GitHub 上公开发布。

![特征匹配结果]({static}/images/sfm/match-output.png)

![特征点选取]({static}/images/sfm/select-points.png)

### LightGlue

LightGlue（Lindenberger et al., ICCV 2023）由 SuperGlue 作者之一 Paul-Edouard Sarlin 参与，ETH Zurich 的 Computer Vision and Geometry Group 提出。它重新审视了 SuperGlue 的多个设计决策并做出改进：

- **自适应推理深度** — 根据图像对的匹配难度动态调整网络层数：容易匹配的图像对提前退出，大幅减少计算量
- **更高的效率** — 在内存和计算量上均优于 SuperGlue
- **更易训练** — 简化了训练流程
- **精度不降反升** — 在多个基准上达到更高匹配精度

这为在 3D 重建等延迟敏感应用中部署深度学习匹配器打开了新的可能。

![SuperGlue 与 LightGlue 对比]({static}/images/sfm/sfm-slide3-img4.png)

![匹配效果展示]({static}/images/sfm/sfm-slide3-img5.png)

## 实验结果

使用实际拍摄的多组图像序列，分别测试了传统 SIFT + 最近邻匹配与 SuperGlue 方案的性能差异：

![实验对比 1]({static}/images/sfm/sfm-slide3-img6.png)

![实验对比 2]({static}/images/sfm/sfm-slide3-img7.png)

![稀疏重建结果]({static}/images/sfm/sfm-slide4-img0.png)

## 总结

| 环节 | 传统方案 | 深度学习方案 |
|------|---------|-------------|
| 特征提取 | SIFT（手工设计） | SuperPoint（自监督 CNN） |
| 特征匹配 | 最近邻 + 比值测试 + RANSAC | SuperGlue / LightGlue（GNN + 最优运输） |
| 遮挡处理 | 启发式阈值 | Dustbin 通道，端到端学习 |
| 计算效率 | CPU 友好 | 需 GPU，LightGlue 可自适应加速 |
| 鲁棒性 | 纹理敏感、大视角退化 | 弱纹理与大视角显著优于传统 |

深度学习特征匹配已成为 SfM 流水线的关键升级方向。在实际项目中，可保持 COLMAP 的重建管线，将特征提取与匹配替换为 SuperPoint + SuperGlue/LightGlue，在弱纹理和大视角场景中获得更稳定、更密集的匹配结果。
