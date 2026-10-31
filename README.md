# 高精度二次元手办 3D 自动化工作流

以原创枫叶女侠 P3 为案例，记录一次真实完成的单图几何生成、独立PBR贴图、可回滚局部修复、Blender摄影与视频交付流程。这里的“高精度”指保留高密度表面和原生纹理并实际检查，不等于已通过打印、绑定或游戏性能验收。

**工作流、离线脚本、真实A2资产包与50秒展示视频现已公开下载。资产包包含可编辑Blender场景和真实A2 GLB，贴图完整内嵌。代码和资产未附MIT/CC开放许可证；公开下载不额外授予商业使用或再分发许可，不自称OSI意义的完整开源项目。**

## 已完成什么

- 原始1122×1402单图 → H3.1 detailed纯几何，实际40积分。
- 灰模验收后 → v3.5 extreme独立PBR贴图，实际30积分。两次明确付费任务合计70积分，没有自动重抽。
- 分离底色、法线、真实几何与遮挡原因，逐次保存V1–V4；最终A2只对已确认下巴区域继续最小修复。
- 从真实A2场景渲染1080×1080、30fps、50秒视频：40秒完整全身360°，3秒推近，7秒面部展示。
- 原文件哈希、打包贴图、几何/UV、完整视频解码与相机轨迹都有核验记录。

这不是“一键生成无瑕疵人物”的宣传：眉上凸脊、部分刘海遮挡、耳前融合界面、发饰接缝和衣领黑破边仍有未解决项。自动几何试验未通过即回滚，最终A2没有采用被拒收的V5/B1几何。

## 阅读顺序

1. [WORKFLOW.md](WORKFLOW.md)：真实流程、失败教训与验收关口。
2. [复现说明](docs/REPRODUCIBILITY.md)：已运行原流程与本次整理工具的验证边界。
3. [资产库存](docs/ASSETS.md)：各文件大小、SHA256及供体/A2身份。
4. [本次验证](docs/VALIDATION.md)。
5. [当前限制](docs/KNOWN_LIMITATIONS.md)、[许可状态](docs/RIGHTS_AND_PUBLICATION.md)。

机器可读参数在[config/run_record.json](config/run_record.json)。工具只读取本地文件、渲染或编码，不包含Tripo提交、凭据解析、自动消费或上传代码。

## 媒体与模型附件

最小模型包包含一个可编辑A2 .blend（7张纹理已打包，含最终镜头）和从真实A2导出的GLB；MP4单独分发，不重复打包摄影场景或纹理。详情见[资产库存](docs/ASSETS.md)和[法线精度等验证边界](docs/VALIDATION.md)。附件已通过[GitHub Release](https://github.com/jackham54321-design/anime-figure-3d-workflow/releases/tag/a2-v1.0.0)发布，不把大型文件写进Git历史。

| 下载 | 大小 | 内容 |
|---|---:|---|
| [A2模型包](https://github.com/jackham54321-design/anime-figure-3d-workflow/releases/download/a2-v1.0.0/Maple_Swordswoman_A2_assets_v1.zip) | 446,058,921 B | 一个.blend、真实A2 GLB、打包贴图和使用/验证说明 |
| [50秒展示视频](https://github.com/jackham54321-design/anime-figure-3d-workflow/releases/download/a2-v1.0.0/A2_360_face_1080_50s.mp4) | 17,257,502 B | 1080×1080、30fps、全身360°与面部展示，无音乐 |
| [SHA256清单](https://github.com/jackham54321-design/anime-figure-3d-workflow/releases/download/a2-v1.0.0/SHA256SUMS) | 192 B | 下载后的完整性校验 |

三份附件已在未登录、无凭据的HTTP请求中完整下载，大小及SHA256均匹配。详见[发布清单](config/release_assets.json)。

AI参与声明：几何与初始PBR纹理由Tripo AI生成；流程整理、Blender脚本和局部检查由人与AI助手协作完成。母图由用户指定为原创角色参考，摄影环境在本地创建。公开下载不额外授予商用/再分发许可，详见许可说明。
