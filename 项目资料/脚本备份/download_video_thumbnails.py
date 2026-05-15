'''
Author: your name
Date: 2026-01-11 01:28:10
LastEditTime: 2026-01-11 01:28:11
LastEditors: your name
Description: In User Settings Edit
FilePath: \Q文件\python_web_project\download_video_thumbnails.py
'''
# -*- coding: utf-8 -*-
"""
下载真实短视频和封面图到本地，并更新数据库
"""
import os
import requests
import random
from urllib.parse import urlparse
from app import app, db
from models import User, Video, Comment
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from utils import save_image, save_file


def download_video_and_thumbnail():
    """下载真实短视频和封面图到本地"""
    with app.app_context():
        # 内置用户名列表
        builtin_users = ['admin', 'tianmi', 'FallPetal', 'zhangsan', 'lisi', 'xiaoming', 'zhaoliu', 'wangwu', 'meimei']
        
        # 真实的短视频链接（使用可访问的公共测试视频）
        video_urls = [
            "https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_1mb.mp4",
            "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
            "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4",
            "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
            "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4",
            "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4",
            "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4",
            "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerMeltdowns.mp4",
            "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4",
        ]
        
        # 真实的缩略图链接（使用可访问的公共图片）
        thumbnail_urls = [
            "https://sample-videos.com/img/Sample_jpg_image_100kb.jpg",
            "https://picsum.photos/400/300?random=1",
            "https://picsum.photos/400/300?random=2",
            "https://picsum.photos/400/300?random=3",
            "https://picsum.photos/400/300?random=4",
            "https://picsum.photos/400/300?random=5",
            "https://picsum.photos/400/300?random=6",
            "https://picsum.photos/400/300?random=7",
            "https://picsum.photos/400/300?random=8",
        ]
        
        # 视频标题列表
        video_titles = [
            "日常生活片段",
            "美食制作教程",
            "风景旅游分享",
            "萌宠可爱瞬间",
            "健身运动指南",
            "手工DIY技巧",
            "音乐才艺展示",
            "搞笑趣事分享",
            "知识科普小课堂"
        ]
        
        # 视频描述列表
        video_descriptions = [
            "分享日常生活中的有趣片段，记录美好时光。",
            "简单易学的美食制作教程，让你在家也能做出美味佳肴。",
            "美丽的风景旅游分享，带你云游世界。",
            "可爱的萌宠瞬间，治愈你的心灵。",
            "科学的健身运动指南，帮助你保持健康体魄。",
            "实用的手工DIY技巧，激发你的创造力。",
            "精彩的音乐才艺展示，享受美妙旋律。",
            "有趣的搞笑趣事分享，让你开怀大笑。",
            "简洁明了的知识科普，拓宽你的视野。"
        ]
        
        # 评论内容列表
        comment_contents = [
            "视频很棒！👍",
            "学到了很多，感谢分享！",
            "拍得真好，已点赞！",
            "期待更多优质内容！",
            "很有意思，已收藏！",
            "制作精良，大力支持！",
            "看完心情愉悦！",
            "非常有用的信息，感谢！",
            "拍摄技术不错，继续加油！",
            "强烈推荐，值得一看！",
            "内容很丰富，收获颇丰！",
            "视频质量很高，清晰流畅！",
            "很喜欢这种风格的内容！",
            "坐等更新，不要鸽哦！",
            "受益匪浅，谢谢博主！",
            "转发了，朋友们都说好！",
            "太有意思了，笑死我了！",
            "干货满满，收藏慢慢看！",
            "技术流，学习了！",
            "感动哭了，太温暖了！"
        ]
        
        # 创建视频和缩略图存储目录
        videos_dir = os.path.join('static', 'uploads', 'videos')
        if not os.path.exists(videos_dir):
            os.makedirs(videos_dir)
        
        # 清除现有的视频和缩略图数据
        existing_videos = Video.query.all()
        for video in existing_videos:
            # 删除对应的文件
            if video.video_url and video.video_url.startswith('uploads/videos/'):
                video_path = os.path.join('static', video.video_url)
                if os.path.exists(video_path):
                    os.remove(video_path)
            if video.thumbnail_url and video.thumbnail_url.startswith('uploads/videos/'):
                thumb_path = os.path.join('static', video.thumbnail_url)
                if os.path.exists(thumb_path):
                    os.remove(thumb_path)
        
        # 删除数据库中的视频和评论
        Comment.query.delete()
        Video.query.delete()
        db.session.commit()
        
        # 为每个内置用户创建视频
        for i, username in enumerate(builtin_users):
            user = User.query.filter_by(username=username).first()
            if user:
                # 选择标题和描述
                title_idx = i % len(video_titles)
                title = f"{video_titles[title_idx]} - {username}"
                description = f"{video_descriptions[title_idx]} 这是用户{username}分享的精彩内容。"
                
                # 选择视频和缩略图URL
                video_url = video_urls[i % len(video_urls)]
                thumbnail_url = thumbnail_urls[i % len(thumbnail_urls)]
                
                try:
                    # 下载视频文件
                    print(f"正在下载视频: {title}")
                    video_response = requests.get(video_url, timeout=30)
                    if video_response.status_code == 200:
                        # 生成唯一的文件名
                        video_filename = f"real_video_{i+1}_{int(datetime.now().timestamp())}.mp4"
                        video_path = os.path.join(videos_dir, video_filename)
                        
                        with open(video_path, 'wb') as f:
                            f.write(video_response.content)
                        
                        # 下载缩略图
                        print(f"正在下载缩略图: {title}")
                        thumb_response = requests.get(thumbnail_url, timeout=30)
                        if thumb_response.status_code == 200:
                            # 生成唯一的缩略图文件名
                            thumb_filename = f"thumb_{i+1}_{int(datetime.now().timestamp())}.jpg"
                            thumb_path = os.path.join(videos_dir, thumb_filename)
                            
                            with open(thumb_path, 'wb') as f:
                                f.write(thumb_response.content)
                            
                            # 生成过去几天到几周内的随机时间戳（模拟真实上传时间）
                            now = datetime.now(ZoneInfo("Asia/Shanghai"))
                            days_back = random.randint(1, 21)
                            hours_back = random.randint(0, 23)
                            minutes_back = random.randint(0, 59)
                            upload_time = now - timedelta(days=days_back, hours=hours_back, minutes=minutes_back)
                            
                            # 创建视频记录
                            video = Video(
                                title=title,
                                description=description,
                                video_url=f"uploads/videos/{video_filename}",
                                thumbnail_url=f"uploads/videos/{thumb_filename}",
                                uploader=user,
                                views=random.randint(100, 10000),  # 随机观看次数
                                likes_count=random.randint(10, 500),  # 随机点赞数
                                timestamp=upload_time  # 使用真实的时间戳
                            )
                            
                            db.session.add(video)
                            db.session.flush()  # 获取视频ID以便创建评论
                            
                            # 为视频创建一些评论（使用真实时间戳）
                            num_comments = random.randint(3, 8)
                            for j in range(num_comments):
                                # 随机选择一个用户作为评论者（可以是其他内置用户）
                                comment_users = User.query.all()
                                comment_user = random.choice(comment_users)
                                
                                comment_content = random.choice(comment_contents)
                                
                                # 生成评论时间戳（在视频上传之后的时间内随机生成）
                                comment_hours_after_upload = random.randint(0, 72)  # 评论在视频上传后最多72小时内
                                comment_minutes_after_upload = random.randint(0, 59)
                                comment_time = upload_time + timedelta(
                                    hours=comment_hours_after_upload, 
                                    minutes=comment_minutes_after_upload
                                )
                                
                                # 确保评论时间不超过当前时间
                                if comment_time > now:
                                    comment_time = now - timedelta(minutes=random.randint(1, 60))
                                
                                comment = Comment(
                                    content=comment_content,
                                    author=comment_user,
                                    video=video,
                                    timestamp=comment_time  # 使用真实的时间戳
                                )
                                
                                db.session.add(comment)
                            
                            print(f"成功为用户 {username} 创建视频: {title} (本地文件: {video_filename})，包含 {num_comments} 条评论")
                        else:
                            print(f"无法下载缩略图: {thumbnail_url}")
                    else:
                        print(f"无法下载视频: {video_url}")
                except Exception as e:
                    print(f"下载视频或缩略图时出错: {str(e)}")
                    # 如果下载失败，创建一个虚拟视频记录
                    video_filename = f"fallback_video_{i+1}.mp4"
                    thumb_filename = f"fallback_thumb_{i+1}.jpg"
                    
                    # 创建虚拟视频文件
                    video_path = os.path.join(videos_dir, video_filename)
                    with open(video_path, 'w') as f:
                        f.write(f"Virtual video file for {title}")
                    
                    # 创建虚拟缩略图文件
                    thumb_path = os.path.join(videos_dir, thumb_filename)
                    with open(thumb_path, 'w') as f:
                        f.write(f"Virtual thumbnail for {title}")
                    
                    # 生成时间戳
                    now = datetime.now(ZoneInfo("Asia/Shanghai"))
                    days_back = random.randint(1, 21)
                    hours_back = random.randint(0, 23)
                    minutes_back = random.randint(0, 59)
                    upload_time = now - timedelta(days=days_back, hours=hours_back, minutes=minutes_back)
                    
                    # 创建视频记录
                    video = Video(
                        title=title,
                        description=description,
                        video_url=f"uploads/videos/{video_filename}",
                        thumbnail_url=f"uploads/videos/{thumb_filename}",
                        uploader=user,
                        views=random.randint(100, 10000),
                        likes_count=random.randint(10, 500),
                        timestamp=upload_time
                    )
                    
                    db.session.add(video)
                    db.session.flush()
                    
                    # 创建评论
                    num_comments = random.randint(3, 8)
                    for j in range(num_comments):
                        comment_users = User.query.all()
                        comment_user = random.choice(comment_users)
                        comment_content = random.choice(comment_contents)
                        
                        comment_hours_after_upload = random.randint(0, 72)
                        comment_minutes_after_upload = random.randint(0, 59)
                        comment_time = upload_time + timedelta(
                            hours=comment_hours_after_upload, 
                            minutes=comment_minutes_after_upload
                        )
                        
                        if comment_time > now:
                            comment_time = now - timedelta(minutes=random.randint(1, 60))
                        
                        comment = Comment(
                            content=comment_content,
                            author=comment_user,
                            video=video,
                            timestamp=comment_time
                        )
                        
                        db.session.add(comment)
                    
                    print(f"使用虚拟文件为用户 {username} 创建视频: {title}")
        
        db.session.commit()
        print("真实视频和缩略图下载完成，数据库已更新")


if __name__ == '__main__':
    download_video_and_thumbnail()