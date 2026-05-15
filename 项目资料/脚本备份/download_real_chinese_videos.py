'''
Author: your name
Date: 2026-01-11 01:35:19
LastEditTime: 2026-01-11 01:35:19
LastEditors: your name
Description: In User Settings Edit
FilePath: \Q文件\python_web_project\download_real_chinese_videos.py
'''
# -*- coding: utf-8 -*-
"""
从国内视频网站下载真实的短视频和封面图到本地
"""
import os
import requests
import random
import re
from urllib.parse import urlparse, parse_qs
from app import app, db
from models import User, Video, Comment
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import time


def extract_video_id_from_url(url):
    """从视频URL中提取视频ID"""
    # 尝试匹配不同视频网站的URL格式
    patterns = [
        r'bilibili\.com/video/(BV\w+)',  # B站BV号
        r'bilibili\.com/video/(av\d+)',  # B站AV号
        r'v\.douyin\.com/(\w+)',        # 抖音
        r'ixigua\.com/(\d+)',           # 西瓜视频
        r'youtube\.com/watch\?v=(\w+)', # YouTube（备用）
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def get_real_video_urls():
    """获取真实的国内视频链接"""
    # 这里列出一些公开的、可访问的国内短视频示例
    # 实际应用中可以通过API获取最新视频
    real_video_sources = [
        {
            "title": "美食制作教程",
            "description": "简单易学的美食制作教程，让你在家也能做出美味佳肴。",
            "video_url": "https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_1mb.mp4",  # 公共测试视频
            "thumb_url": "https://picsum.photos/400/300?random=1"
        },
        {
            "title": "风景旅游分享", 
            "description": "美丽的风景旅游分享，带你云游世界。",
            "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",  # 公共测试视频
            "thumb_url": "https://picsum.photos/400/300?random=2"
        },
        {
            "title": "萌宠可爱瞬间",
            "description": "可爱的萌宠瞬间，治愈你的心灵。",
            "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4",  # 公共测试视频
            "thumb_url": "https://picsum.photos/400/300?random=3"
        },
        {
            "title": "健身运动指南",
            "description": "科学的健身运动指南，帮助你保持健康体魄。",
            "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",  # 公共测试视频
            "thumb_url": "https://picsum.photos/400/300?random=4"
        },
        {
            "title": "手工DIY技巧",
            "description": "实用的手工DIY技巧，激发你的创造力。",
            "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4",  # 公共测试视频
            "thumb_url": "https://picsum.photos/400/300?random=5"
        },
        {
            "title": "音乐才艺展示",
            "description": "精彩的音乐才艺展示，享受美妙旋律。",
            "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4",  # 公共测试视频
            "thumb_url": "https://picsum.photos/400/300?random=6"
        },
        {
            "title": "搞笑趣事分享",
            "description": "有趣的搞笑趣事分享，让你开怀大笑。",
            "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4",  # 公共测试视频
            "thumb_url": "https://picsum.photos/400/300?random=7"
        },
        {
            "title": "知识科普小课堂",
            "description": "简洁明了的知识科普，拓宽你的视野。",
            "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerMeltdowns.mp4",  # 公共测试视频
            "thumb_url": "https://picsum.photos/400/300?random=8"
        },
        {
            "title": "日常生活片段",
            "description": "分享日常生活中的有趣片段，记录美好时光。",
            "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4",  # 公共测试视频
            "thumb_url": "https://picsum.photos/400/300?random=9"
        }
    ]
    
    return real_video_sources


def download_real_chinese_videos():
    """下载真实的国内视频和封面到本地"""
    with app.app_context():
        # 内置用户名列表
        builtin_users = ['admin', 'tianmi', 'FallPetal', 'zhangsan', 'lisi', 'xiaoming', 'zhaoliu', 'wangwu', 'meimei']
        
        # 获取真实的视频源
        real_video_sources = get_real_video_urls()
        
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
        
        # 尝试下载每个视频
        successful_downloads = 0
        
        for i, user_data in enumerate(real_video_sources):
            username = builtin_users[i] if i < len(builtin_users) else builtin_users[0]
            user = User.query.filter_by(username=username).first()
            
            if user:
                title = f"{user_data['title']} - {username}"
                description = f"{user_data['description']} 这是用户{username}分享的精彩内容。"
                
                video_url = user_data['video_url']
                thumb_url = user_data['thumb_url']
                
                try:
                    # 下载视频文件
                    print(f"正在下载视频: {title}")
                    video_response = requests.get(video_url, timeout=60, stream=True)
                    
                    if video_response.status_code == 200:
                        # 生成唯一的文件名
                        video_filename = f"chinese_video_{i+1}_{int(time.time())}.mp4"
                        video_path = os.path.join(videos_dir, video_filename)
                        
                        # 流式下载视频文件
                        with open(video_path, 'wb') as f:
                            for chunk in video_response.iter_content(chunk_size=8192):
                                f.write(chunk)
                        
                        # 下载缩略图
                        print(f"正在下载缩略图: {title}")
                        thumb_response = requests.get(thumb_url, timeout=30)
                        
                        if thumb_response.status_code == 200:
                            # 生成唯一的缩略图文件名
                            thumb_filename = f"chinese_thumb_{i+1}_{int(time.time())}.jpg"
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
                            
                            print(f"✅ 成功为用户 {username} 创建视频: {title} (本地文件: {video_filename})，包含 {num_comments} 条评论")
                            successful_downloads += 1
                        else:
                            print(f"❌ 无法下载缩略图: {thumb_url}")
                    else:
                        print(f"❌ 无法下载视频: {video_url}")
                        # 如果下载失败，跳过这次循环
                        continue
                        
                except requests.exceptions.RequestException as e:
                    print(f"❌ 下载视频或缩略图时网络错误: {str(e)}")
                    continue
                except Exception as e:
                    print(f"❌ 下载视频或缩略图时出现错误: {str(e)}")
                    continue
        
        db.session.commit()
        
        if successful_downloads > 0:
            print(f"\n🎉 成功下载并保存了 {successful_downloads} 个真实视频和封面图！")
            print("所有文件已保存到本地，数据库已更新。")
        else:
            print(f"\n❌ 未能成功下载任何视频，请检查网络连接和视频链接的有效性。")
            
            # 作为备选方案，创建最小化的演示视频
            print("正在创建备选方案的演示视频...")
            create_demo_videos()


def create_demo_videos():
    """创建最小化的演示视频作为备选方案"""
    import cv2
    import numpy as np
    
    with app.app_context():
        builtin_users = ['admin', 'tianmi', 'FallPetal', 'zhangsan', 'lisi', 'xiaoming', 'zhaoliu', 'wangwu', 'meimei']
        
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
        
        videos_dir = os.path.join('static', 'uploads', 'videos')
        
        # 创建演示视频
        for i, username in enumerate(builtin_users):
            user = User.query.filter_by(username=username).first()
            if user and i < len(video_titles):
                title = f"{video_titles[i]} - {username}"
                description = f"{video_descriptions[i]} 这是用户{username}分享的精彩内容。"
                
                # 创建视频文件
                video_filename = f"demo_video_{i+1}_{int(time.time())}.mp4"
                video_path = os.path.join(videos_dir, video_filename)
                
                # 使用OpenCV创建简单的演示视频
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                fps = 24
                duration = 15  # 15秒
                width, height = 640, 480
                out = cv2.VideoWriter(video_path, fourcc, fps, (width, height))
                
                for frame_num in range(fps * duration):
                    # 创建渐变背景
                    img = np.zeros((height, width, 3), np.uint8)
                    
                    # 动态颜色
                    color_val = int(100 + 100 * (frame_num % fps) / fps)
                    img[:] = [max(0, 200 - color_val), min(255, color_val), 150]
                    
                    # 添加标题文本
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    text = title
                    font_scale = 0.8
                    thickness = 2
                    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
                    text_x = (width - text_size[0]) // 2
                    text_y = height // 2
                    
                    cv2.putText(img, text, (text_x, text_y), font, font_scale, (255, 255, 255), thickness)
                    
                    # 添加副标题
                    subtitle = f"第 {frame_num // fps + 1} 秒 / 共 {duration} 秒"
                    sub_font_scale = 0.6
                    sub_thickness = 1
                    sub_text_size = cv2.getTextSize(subtitle, font, sub_font_scale, sub_thickness)[0]
                    sub_text_x = (width - sub_text_size[0]) // 2
                    sub_text_y = text_y + 50
                    
                    cv2.putText(img, subtitle, (sub_text_x, sub_text_y), font, sub_font_scale, (200, 200, 200), sub_thickness)
                    
                    out.write(img)
                
                out.release()
                
                # 创建缩略图
                from PIL import Image, ImageDraw
                
                thumb_filename = f"demo_thumb_{i+1}_{int(time.time())}.jpg"
                thumb_path = os.path.join(videos_dir, thumb_filename)
                
                img = Image.new('RGB', (400, 300), color=(73, 109, 137))
                d = ImageDraw.Draw(img)
                
                # 绘制渐变背景
                for y in range(300):
                    r = int(73 + (182-73) * y / 300)
                    g = int(109 + (137-109) * y / 300)
                    b = int(137 + (204-137) * y / 300)
                    d.line([(0, y), (400, y)], fill=(r, g, b))
                
                # 添加标题文本
                try:
                    from PIL import ImageFont
                    font = ImageFont.load_default()
                except:
                    font = None
                
                title_lines = [title[j:j+10] for j in range(0, len(title), 10)]
                y_offset = 100
                for line in title_lines:
                    d.text(((400 - 100) // 2, y_offset), line, fill=(255, 255, 255), font=font)
                    y_offset += 25
                
                # 添加播放图标
                d.polygon([(150, 130), (150, 170), (180, 150)], fill=(255, 255, 255, 128))
                
                img.save(thumb_path)
                
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
                
                print(f"✅ 已创建演示视频: {title}")
        
        db.session.commit()
        print("✅ 备选方案完成：已创建演示视频和缩略图")


if __name__ == '__main__':
    download_real_chinese_videos()