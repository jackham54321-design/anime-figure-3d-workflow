# 复现与验证边界

## 环境和资产

历史原流程已在Blender 5.2.3 LTS、EEVEE、Metal/Apple M5、FFmpeg 9.0.1运行。独立编码/检验工具需要Python 3.11或更新版本；渲染工具使用Blender自带Python/NumPy。仓库不安装软件，不提供凭据或收费API客户端。`config/run_record.json`记录历史真实参数，云服务价格/版本可能改变。

模型和视频不进入Git历史。最小Release包已在本地准备，附件实际上传后可解压到`assets/Maple_Swordswoman_A2/`；校验SHA256并使用`model/Maple_Swordswoman_A2.blend`。该独立脱敏场景已打包7张纹理，同时保留最终50秒相机动画，无需作者私有目录。GLB只含模型，无摄影镜头；重现影片使用.blend。当前尚未上传Release附件。

## 新的可移植工具

本次从已跑通流程抽出三份不联网工具；它们是整理后的实现，不冒充曾用于完整1500帧的逐字原脚本。只读检查与视频核验会单独执行，未为写仓库重新渲染1500帧。

```bash
# 只读核对场景；不会渲染或保存.blend
blender --background --factory-startup --disable-autoexec --python scripts/render_saved_scene.py -- --scene assets/Maple_Swordswoman_A2/model/Maple_Swordswoman_A2.blend --output output --inspect-only

# 后续自愿执行，实际会渲染；本次仓库准备没有执行此行
blender --background --factory-startup --disable-autoexec --python scripts/render_saved_scene.py -- --scene assets/Maple_Swordswoman_A2/model/Maple_Swordswoman_A2.blend --output output

python3 scripts/encode_video.py --frames output/frames --output output/A2_360_face_1080_50s.mp4
python3 scripts/verify_video.py output/A2_360_face_1080_50s.mp4
```

渲染工具使用保存的真实相机动画，保持场景参数和资产不变；同一输出目录使用排他锁，校验已完成PNG前缀，损坏/缺口停止，不覆盖文件。原片和新输出分开。源场景哈希在前后核对，不保存场景。不对其它平台的数值结果作保证。

编码保留原实际sRGB PNG到BT.709 limited转换、H.264 CRF16/medium/yuv420p、faststart、无音轨。检验工具检查1500帧/50秒/30fps/1080方、色彩标签、PTS、完整解码与SHA；艺术验收还需实际查看全身各方位、脸部、剑刃和连续转场。

## 无法一步复现的部分

- 原始云端任务需要用户自己的合法授权、登录、上传同意和逐笔费用确认；这里只记录流程，不自动提交。
- V1–V4/A2修补是特定模型的语义面片/UV决策，不是通用自动修脸插件；不能套屏幕矩形或旧面索引到新模型。
- 1500张PNG与重型诊断已按用户要求可恢复清理；公开文档只包含精简验收结果，没有重新恢复中间文件。
- 已完成真实A2 GLB导出与干净重导入；几何/UV/纹理一致，但法线有已记录精度差异，不能宣称所有属性逐位相等。
- 当前官方中国API条款的付费输出分发依据与项目实际附件状态分开记录，见许可页；没有以公开临时托管替代正式交付。
