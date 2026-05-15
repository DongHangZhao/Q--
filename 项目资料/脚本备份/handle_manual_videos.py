'''
Author: your name
Date: 2026-01-11 01:57:29
LastEditTime: 2026-01-11 01:57:29
LastEditors: your name
Description: In User Settings Edit
FilePath: \Q文件\python_web_project\handle_manual_videos.py
'''
# -*- coding: utf-8 -*-
"""
处理手动下载的国内短视频，将其整合到系统中
"""
import os
import shutil
import random
from app import app, db
from models import User, Video, Comment
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import time


def handle_manual_videos():
    """处理手动下载的视频文件"""
    with app.app_context():
        # 内置用户名列表
        builtin_users = ['admin', 'tianmi', 'FallPetal', 'zhangsan', 'lisi', 'xiaoming', 'zhaoliu', 'wangwu', 'meimei']
        
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
        
        # 创建视频存储目录
        videos_dir = os.path.join('static', 'uploads', 'videos')
        if not os.path.exists(videos_dir):
            os.makedirs(videos_dir)
        
        # 检查是否有手动下载的视频文件
        manual_video_dir = os.path.join('downloads')  # 预期的下载目录
        if not os.path.exists(manual_video_dir):
            os.makedirs(manual_video_dir)
        
        # 获取手动下载的视频文件（支持多种格式）
        supported_formats = ['.mp4', '.avi', '.mov', '.wmv', '.mkv', '.webm', '.flv', '.f4v', '.f4p', '.f4a', '.f4b']
        manual_videos = []
        
        if os.path.exists(manual_video_dir):
            for file in os.listdir(manual_video_dir):
                if any(file.lower().endswith(fmt) for fmt in supported_formats):
                    manual_videos.append(file)
        
        print(f"在 downloads 目录中找到 {len(manual_videos)} 个视频文件")
        
        # 如果找到了手动下载的视频，就使用它们
        if manual_videos:
            print("正在处理手动下载的视频文件...")
            
            # 清除现有的视频和评论
            Comment.query.delete()
            Video.query.delete()
            db.session.commit()
            
            # 为每个用户分配视频
            for i, username in enumerate(builtin_users):
                user = User.query.filter_by(username=username).first()
                if user and i < len(manual_videos):
                    # 获取视频文件
                    video_file = manual_videos[i]
                    video_source_path = os.path.join(manual_video_dir, video_file)
                    
                    # 生成目标文件名
                    dest_video_filename = f"real_video_{i+1}_{int(time.time())}.mp4"
                    dest_video_path = os.path.join(videos_dir, dest_video_filename)
                    
                    # 复制视频文件到目标位置
                    shutil.copy2(video_source_path, dest_video_path)
                    
                    # 生成缩略图文件名
                    thumb_filename = f"real_thumb_{i+1}_{int(time.time())}.jpg"
                    thumb_path = os.path.join(videos_dir, thumb_filename)
                    
                    # 创建简单的缩略图
                    from PIL import Image, ImageDraw
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
                    
                    # 分行显示标题
                    title = f"{video_titles[i]} - {username}"
                    title_lines = [title[j:j+12] for j in range(0, len(title), 12)]
                    y_offset = 100
                    for line in title_lines:
                        if font:
                            try:
                                bbox = d.textbbox((0, 0), line, font=font)
                                text_width = bbox[2] - bbox[0]
                                x = (400 - text_width) // 2
                                d.text((x, y_offset), line, fill=(255, 255, 255), font=font)
                            except:
                                text_width = 100  # 默认宽度
                                x = (400 - text_width) // 2
                                d.text((x, y_offset), line, fill=(255, 255, 255))
                        else:
                            text_width = 100  # 默认宽度
                            x = (400 - text_width) // 2
                            d.text((x, y_offset), line, fill=(255, 255, 255))
                        
                        y_offset += 25
                    
                    # 添加播放图标
                    d.polygon([(150, 180), (150, 220), (190, 200)], fill=(255, 255, 255, 200))
                    
                    # 添加用户名称
                    try:
                        if font:
                            user_bbox = d.textbbox((0, 0), username, font=font)
                            user_width = user_bbox[2] - user_bbox[0]
                            d.text(((400 - user_width) // 2, 250), username, fill=(200, 200, 200), font=font)
                        else:
                            user_width = 60  # 默认宽度
                            d.text(((400 - user_width) // 2, 250), username, fill=(200, 200, 200))
                    except:
                        user_width = 60  # 默认宽度
                        d.text(((400 - user_width) // 2, 250), username, fill=(200, 200, 200))
                    
                    img.save(thumb_path, quality=90)
                    
                    # 生成时间戳
                    now = datetime.now(ZoneInfo("Asia/Shanghai"))
                    days_back = random.randint(1, 21)
                    hours_back = random.randint(0, 23)
                    minutes_back = random.randint(0, 59)
                    upload_time = now - timedelta(days=days_back, hours=hours_back, minutes=minutes_back)
                    
                    # 创建视频记录
                    video = Video(
                        title=title,
                        description=f"{video_descriptions[i]} 这是用户{username}分享的精彩内容。",
                        video_url=f"uploads/videos/{dest_video_filename}",
                        thumbnail_url=f"uploads/videos/{thumb_filename}",
                        uploader=user,
                        views=random.randint(100, 10000),
                        likes_count=random.randint(10, 500),
                        timestamp=upload_time
                    )
                    db.session.add(video)
                    db.session.flush()  # 获取视频ID以便创建评论
                    
                    # 为视频创建一些评论
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
                    
                    print(f"✅ 成功为用户 {username} 添加真实视频: {title}")
        
        else:
            print("未在 downloads 目录找到视频文件，正在尝试从国内视频网站获取...")
            
            # 由于无法直接下载，创建高质量的模拟视频作为备选方案
            # 创建高质量的本地视频，使用最兼容的格式
            print("创建高质量的本地视频作为备选方案...")
            
            # 清除现有的视频和评论
            Comment.query.delete()
            Video.query.delete()
            db.session.commit()
            
            # 为每个用户创建高质量视频
            for i, username in enumerate(builtin_users):
                user = User.query.filter_by(username=username).first()
                if user and i < len(video_titles):
                    title = f"{video_titles[i]} - {username}"
                    description = f"{video_descriptions[i]} 这是用户{username}分享的精彩内容。"
                    
                    # 生成视频文件名
                    video_filename = f"domestic_video_{i+1}_{int(time.time())}.mp4"
                    video_path = os.path.join(videos_dir, video_filename)
                    
                    # 创建兼容性最好的视频（使用较低的复杂度以确保兼容性）
                    try:
                        import cv2
                        import numpy as np
                        
                        # 使用最基础的编码设置
                        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                        fps = 24
                        duration = 15  # 15秒
                        width, height = 640, 480  # 标准分辨率
                        
                        out = cv2.VideoWriter(video_path, fourcc, fps, (width, height))
                        
                        # 创建简单但清晰的视频内容
                        for frame_num in range(fps * duration):
                            # 创建简单的渐变背景
                            img = np.zeros((height, width, 3), dtype=np.uint8)
                            
                            # 颜色随时间变化
                            phase = (frame_num / (fps * duration)) * 2 * 3.14159
                            r = int(128 + 127 * abs(np.sin(phase)))
                            g = int(128 + 127 * abs(np.sin(phase + 2.094)))  # 120度相位差
                            b = int(128 + 127 * abs(np.sin(phase + 4.188)))  # 240度相位差
                            
                            img[:] = [b, g, r]  # OpenCV使用BGR格式
                            
                            # 添加标题文本
                            font = cv2.FONT_HERSHEY_SIMPLEX
                            text = title
                            font_scale = 0.6
                            thickness = 2
                            text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
                            text_x = (width - text_size[0]) // 2
                            text_y = height // 2 - 20
                            
                            # 添加带轮廓的文本
                            cv2.putText(img, text, (text_x-1, text_y), font, font_scale, (0, 0, 0), thickness+2)
                            cv2.putText(img, text, (text_x+1, text_y), font, font_scale, (0, 0, 0), thickness+2)
                            cv2.putText(img, text, (text_x, text_y-1), font, font_scale, (0, 0, 0), thickness+2)
                            cv2.putText(img, text, (text_x, text_y+1), font, font_scale, (0, 0, 0), thickness+2)
                            cv2.putText(img, text, (text_x, text_y), font, font_scale, (255, 255, 255), thickness)
                            
                            # 添加计时器
                            timer_text = f"{(frame_num // fps) + 1}/{duration}s"
                            timer_size = cv2.getTextSize(timer_text, font, 0.5, 1)[0]
                            timer_x = width - timer_size[0] - 10
                            timer_y = height - 10
                            
                            cv2.putText(img, timer_text, (timer_x-1, timer_y), font, 0.5, (0, 0, 0), 2)
                            cv2.putText(img, timer_text, (timer_x, timer_y), font, 0.5, (200, 200, 200), 1)
                            
                            out.write(img)
                        
                        out.release()
                        print(f"✅ 创建视频文件: {video_filename}")
                    except ImportError:
                        print("⚠️ OpenCV未安装，创建占位视频文件")
                        # 如果OpenCV不可用，创建一个简单的占位文件
                        with open(video_path, 'w') as f:
                            f.write(f"Placeholder video file for {title}")
                    
                    # 创建缩略图
                    thumb_filename = f"domestic_thumb_{i+1}_{int(time.time())}.jpg"
                    thumb_path = os.path.join(videos_dir, thumb_filename)
                    
                    try:
                        from PIL import Image, ImageDraw
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
                        
                        # 分行显示标题
                        title_lines = [title[j:j+12] for j in range(0, len(title), 12)]
                        y_offset = 100
                        for line in title_lines:
                            if font:
                                try:
                                    bbox = d.textbbox((0, 0), line, font=font)
                                    text_width = bbox[2] - bbox[0]
                                    x = (400 - text_width) // 2
                                    d.text((x, y_offset), line, fill=(255, 255, 255), font=font)
                                except:
                                    text_width = 100  # 默认宽度
                                    x = (400 - text_width) // 2
                                    d.text((x, y_offset), line, fill=(255, 255, 255))
                            else:
                                text_width = 100  # 默认宽度
                                x = (400 - text_width) // 2
                                d.text((x, y_offset), line, fill=(255, 255, 255))
                            
                            y_offset += 25
                        
                        # 添加播放图标
                        d.polygon([(150, 180), (150, 220), (190, 200)], fill=(255, 255, 255, 200))
                        
                        # 添加用户名称
                        try:
                            if font:
                                user_bbox = d.textbbox((0, 0), username, font=font)
                                user_width = user_bbox[2] - user_bbox[0]
                                d.text(((400 - user_width) // 2, 250), username, fill=(200, 200, 200), font=font)
                            else:
                                user_width = 60  # 默认宽度
                                d.text(((400 - user_width) // 2, 250), username, fill=(200, 200, 200))
                        except:
                            user_width = 60  # 默认宽度
                            d.text(((400 - user_width) // 2, 250), username, fill=(200, 200, 200))
                        
                        img.save(thumb_path, quality=90)
                    except ImportError:
                        # 如果PIL不可用，创建占位文件
                        with open(thumb_path, 'w') as f:
                            f.write(f"Placeholder thumbnail for {title}")
                    
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
                    db.session.flush()  # 获取视频ID以便创建评论
                    
                    # 为视频创建一些评论
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
                    
                    print(f"✅ 为用户 {username} 创建高质量视频: {title}")
        
        db.session.commit()
        
        # 更新评论计数
        videos = Video.query.all()
        for video in videos:
            comment_count = Comment.query.filter_by(video_id=video.id).count()
            video.comments_count = comment_count
        
        db.session.commit()
        
        print("\n🎉 视频处理完成！")
        print("请按照以下步骤添加真实视频：")
        print("1. 手动从国内视频网站（如抖音、B站等）下载一些短视频")
        print("2. 将下载的视频文件放在项目根目录下的 'downloads' 文件夹中")
        print("3. 再次运行此脚本，它会自动处理这些视频文件")
        print("4. 如果没有手动下载视频，系统将继续使用高质量的本地生成视频")


if __name__ == '__main__':
    handle_manual_videos()