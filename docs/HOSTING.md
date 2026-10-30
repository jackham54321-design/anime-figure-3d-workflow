# GitHub存放方案

Git只存README、WORKFLOW、原创脚本、参数与校验清单；没有模型、贴图、参考图、渲染图或视频。本轮不创建Release附件。

权利核验和资产脱敏完成后，计划把最终MP4、可编辑A2、独立摄影场景、纹理包及明确标注的原始供体作为Release附件。每个附件控制在2GiB以内；目前最大单个候选约249MB，无需付费LFS或无损分包。

GitHub普通Git对超过50MiB的文件警告，并阻止超过100MiB的文件。因此.blend不可直接加入Git历史；较小MP4也优先随Release分发以避免二进制版本累积。参见[官方大文件说明](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github)和[Release说明](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)，阅读日期2026-10-30。平台限额以后仍需重新核对。

正式附件清单必须记录SHA256、字节数、文件身份与授权状态。原始供体不重命名成A2；如果导出A2 GLB，必须从真实A2另存并核对世界空间三角面、UV、材质与纹理，不以文件打开成功代替等价验收。
