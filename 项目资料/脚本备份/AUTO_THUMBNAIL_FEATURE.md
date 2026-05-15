# 自动视频封面生成功能

## 功能说明
系统现在具备自动从视频中提取帧作为封面的功能，确保每个视频都有对应的封面图像。

## 实现方式
- 当用户上传视频时，如果未提供缩略图，系统会自动从视频中提取一帧作为封面
- 使用OpenCV从视频中随机选择中间80%部分的帧，避免开头和结尾的黑屏
- 生成的封面为JPEG格式，最大尺寸为400x400像素

## 已更新的视频
- 日常生活片段 - admin
- 美食制作教程 - tianmi
- 风景旅游分享 - FallPetal
- 萌宠可爱瞬间 - zhangsan

## 代码变更
- 在[app.py](file:///e:/办公练习/Html/Q文件/python_web_project/app.py)中添加了`extract_frame_as_thumbnail`函数
- 修改了视频上传路由`/video`，增加了自动封面生成功能
- 创建了[update_real_video_thumbnails.py](file:///e:/办公练习/Html/Q文件/python_web_project/update_real_video_thumbnails.py)脚本来更新现有视频的封面路径

## 优势
- 确保所有视频都有封面，提升用户体验
- 无需手动为每个视频创建封面
- 自动生成的封面与视频内容相关，更加真实
- 适用于所有新上传的视频