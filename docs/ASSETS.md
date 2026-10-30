# 本地真实资产库存

下表为未公开的原始候选。SHA256对应未脱敏源副本；将来若清理.blend元数据，发布副本需另记新哈希。A2包含7张已打包图像，无外链Blend库；其中4张修复纹理也保留外部文件。V4完整回滚仍保留在本地，不作为本次默认公开附件。

| 候选文件 | 字节 | 用途 |
|---|---:|---|
| `A2_360_face_1080_50s.mp4` | 17,257,502 | 最终真实模型展示视频 |
| `maple_p3_chin_A2.blend` | 248,740,795 | 已接受的可编辑A2；不是原始Tripo供体 |
| `A2_360_face_50s.blend` | 248,843,303 | 完整相机动画和外部摄影场景 |
| `source_geometry.glb` | 56,451,816 | 原始无贴图供体；不是A2 |
| `source_textured.glb` | 79,705,056 | 原始PBR供体；不含V1–V4/A2局部修复 |
| `reference_P3.png` | 2,163,816 | 原始用户母图，未经裁切或增强 |
| `textures/base_color_A2.png` | 63,516,291 | A2隔离下巴材质底色 |
| `textures/normal_A1.png` | 4,753,467 | A2隔离下巴材质法线 |
| `textures/base_color_v4.png` | 63,516,290 | V4主要底色；被A2引用 |
| `textures/normal_local_v4.png` | 4,753,476 | V4局部修正法线；被A2引用 |

精确SHA256见[asset_inventory.json](../config/asset_inventory.json)。所有附件当前处于暂缓公开状态。原始灰模、彩色供体及A2不能互相替代；没有A2 GLB导出。
