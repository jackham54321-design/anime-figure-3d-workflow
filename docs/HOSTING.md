# GitHub存放方案

Git只存README、WORKFLOW、原创脚本、参数与校验清单。大型资产使用Release附件，不使用付费LFS，不把.blend/GLB/MP4塞入Git历史。

最小模型ZIP包含一个已打包贴图的A2 .blend（含最终摄影镜头）、真实A2 GLB和必要说明。最终MP4独立附上；不重复附第二份原生场景和外部纹理。每件附件小于2GiB，不需分包。当前文件已在本地准备，尚未上传Release。

参见[GitHub大文件说明](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github)和[Release说明](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)，核对日期2026-10-30。未来平台限额应重新核对。

每份附件有字节数、SHA256、文件身份和验证范围。原始供体不冒充A2；纹理及几何相同不意味着所有法线浮点编码相同。
