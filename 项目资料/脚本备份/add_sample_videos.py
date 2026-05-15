'''
Author: your name
Date: 2026-01-11 01:07:13
LastEditTime: 2026-01-11 01:07:13
LastEditors: your name
Description: In User Settings Edit
FilePath: \Q文件\python_web_project\add_sample_videos.py
'''
"""
为内置用户添加示例视频记录
"""
from app import app, db
from models import User, Video
import os


def add_sample_videos():
    """为内置用户添加示例视频记录"""
    with app.app_context():
        # 创建视频目录
        videos_dir = 'static/uploads/videos'
        if not os.path.exists(videos_dir):
            os.makedirs(videos_dir)
        
        # 内置用户名列表
        builtin_users = ['admin', 'tianmi', 'FallPetal', 'zhangsan', 'lisi', 'xiaoming', 'zhaoliu', 'wangwu', 'meimei']
        
        # 创建示例视频文件（空文件或使用默认视频）
        sample_video_files = []
        for i in range(len(builtin_users)):
            video_filename = f"sample_video_{i+1}.mp4"
            filepath = os.path.join(videos_dir, video_filename)
            
            # 创建一个空的示例视频文件（实际应用中这里应该是真实视频）
            with open(filepath, 'w') as f:
                f.write(f"Sample video content for video {i+1}")
            
            sample_video_files.append(video_filename)
        
        # 为每个内置用户创建一个视频
        for i, username in enumerate(builtin_users):
            user = User.query.filter_by(username=username).first()
            if user and i < len(sample_video_files):
                video_filename = sample_video_files[i]
                video_title = f"{username}的视频 {i+1}"
                video_description = f"这是用户{username}上传的示例视频"
                
                # 检查是否已经存在该用户的视频
                existing_video = Video.query.filter_by(title=video_title).first()
                if not existing_video:
                    # 创建视频记录
                    video = Video(
                        title=video_title,
                        description=video_description,
                        video_url=f"uploads/videos/{video_filename}",
                        uploader=user
                    )
                    
                    db.session.add(video)
                    print(f"为用户 {username} 创建视频: {video_title}")
                else:
                    print(f"用户 {username} 的视频已存在: {video_title}")
        
        db.session.commit()
        print("示例视频记录添加完成")


if __name__ == '__main__':
    add_sample_videos()