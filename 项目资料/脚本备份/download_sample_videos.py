'''
Author: your name
Date: 2026-01-11 01:05:19
LastEditTime: 2026-01-11 01:05:19
LastEditors: your name
Description: In User Settings Edit
FilePath: \Q文件\python_web_project\download_sample_videos.py
'''
"""
下载示例短视频并分配给内置用户
"""
import os
import requests
from app import app, db
from models import User, Video
import random


def download_sample_videos():
    """下载示例短视频"""
    with app.app_context():
        # 创建视频目录
        videos_dir = 'static/uploads/videos'
        if not os.path.exists(videos_dir):
            os.makedirs(videos_dir)
        
        # 示例视频URL列表（使用一些公共的短视频示例）
        sample_video_urls = [
            "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
            "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4",
            "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4",
            "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4",
            "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerMeltdowns.mp4",
        ]
        
        # 内置用户名列表
        builtin_users = ['admin', 'tianmi', 'FallPetal', 'zhangsan', 'lisi', 'xiaoming', 'zhaoliu', 'wangwu', 'meimei']
        
        downloaded_videos = []
        
        # 下载视频文件
        for i, url in enumerate(sample_video_urls):
            try:
                print(f"正在下载视频 {i+1}...")
                response = requests.get(url, stream=True)
                if response.status_code == 200:
                    # 只下载前几MB用于演示（短视频）
                    max_size = 10 * 1024 * 1024  # 10MB限制
                    downloaded_size = 0
                    filename = f"sample_video_{i+1}.mp4"
                    filepath = os.path.join(videos_dir, filename)
                    
                    with open(filepath, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                                downloaded_size += len(chunk)
                                if downloaded_size >= max_size:
                                    print(f"达到大小限制，截取视频 {filename}")
                                    break
                    
                    downloaded_videos.append(filename)
                    print(f"下载完成: {filename}")
                else:
                    print(f"下载失败: {url}")
            except Exception as e:
                print(f"下载出错 {url}: {str(e)}")
        
        # 为内置用户分配视频
        for i, username in enumerate(builtin_users):
            user = User.query.filter_by(username=username).first()
            if user and i < len(downloaded_videos):
                video_filename = downloaded_videos[i]
                video_title = f"{username}的视频 {i+1}"
                video_description = f"这是用户{username}的示例视频"
                
                # 创建视频记录
                video = Video(
                    title=video_title,
                    description=video_description,
                    video_url=f"uploads/videos/{video_filename}",
                    uploader=user
                )
                
                db.session.add(video)
                print(f"为用户 {username} 创建视频: {video_title}")
        
        db.session.commit()
        print("示例视频下载和分配完成")


if __name__ == '__main__':
    download_sample_videos()