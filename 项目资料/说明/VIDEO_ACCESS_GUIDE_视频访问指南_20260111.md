# 真实视频访问指南

## 服务器状态
✅ Web服务器正在运行
🌐 访问地址：http://localhost:5000
📱 局域网访问：http://192.168.2.182:5000

## 内置用户账号
您可以使用以下任意一个内置用户账号登录系统：

| 用户名 | 状态 |
|--------|------|
| admin | 已分配真实视频 |
| tianmi | 已分配真实视频 |
| FallPetal | 已分配真实视频 |
| zhangsan | 已分配真实视频 |
| lisi | 可用 |
| xiaoming | 可用 |
| zhaoliu | 可用 |
| wangwu | 可用 |
| meimei | 可用 |

## 视频信息
系统当前包含4个来自国内视频网站的真实视频：

1. **admin的视频**：日常生活片段 (约2.15MB)
2. **tianmi的视频**：美食制作教程 (约0.28MB) 
3. **FallPetal的视频**：风景旅游分享 (约0.51MB)
4. **zhangsan的视频**：萌宠可爱瞬间 (约11.6MB)

## 如何查看视频
1. 打开浏览器并访问 http://localhost:5000
2. 点击右上角的"登录"按钮
3. 使用以上任一用户名和任意密码（系统未设置密码验证）登录
4. 登录后即可在首页看到分配给该用户的视频
5. 点击视频可以播放，点击视频下方可以查看相关评论

## 添加更多视频
如果您想添加更多来自国内视频网站的真实视频：

1. 手动从抖音、B站等平台下载短视频
2. 将视频文件放入 [downloads](file:///e:/办公练习/Html/Q文件/python_web_project/downloads) 目录
3. 停止当前服务器（Ctrl+C）
4. 运行处理脚本：`python handle_manual_videos.py`
5. 重新启动服务器：`python run.py`

## 问题排查
如果视频无法播放：
- 确认服务器正在运行
- 检查浏览器是否支持MP4格式
- 验证视频文件是否存在：[static/uploads/videos](file:///e:/办公练习/Html/Q文件/python_web_project/static/uploads/videos)

## 停止服务器
要停止服务器，请在终端中按下 Ctrl+C。