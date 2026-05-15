'''
Author: your name
Date: 2026-01-11 01:29:48
LastEditTime: 2026-01-11 01:29:49
LastEditors: your name
Description: In User Settings Edit
FilePath: \Q文件\python_web_project\create_local_video_thumbnails.py
'''
# -*- coding: utf-8 -*-
"""
在无法访问外部网络时，创建本地短视频和封面图文件，并更新数据库
"""
import os
import random
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
from app import app, db
from models import User, Video, Comment
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


def create_local_video_thumbnails():
    """创建本地短视频和封面图文件，并更新数据库"""
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
        
        # 为每个内置用户创建视频和封面图
        for i, username in enumerate(builtin_users):
            user = User.query.filter_by(username=username).first()
            if user:
                # 选择标题和描述
                title_idx = i % len(video_titles)
                title = f"{video_titles[title_idx]} - {username}"
                description = f"{video_descriptions[title_idx]} 这是用户{username}分享的精彩内容。"
                
                # 生成唯一的视频文件名
                video_filename = f"local_video_{i+1}_{int(datetime.now().timestamp())}.mp4"
                video_path = os.path.join(videos_dir, video_filename)
                
                # 创建简单的本地视频文件
                # 使用OpenCV创建一个简单的视频
                try:
                    # 创建一个简单的视频 - 10秒长，30fps，分辨率为480x320
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                    fps = 30
                    duration = 10  # 10秒
                    width, height = 640, 480
                    out = cv2.VideoWriter(video_path, fourcc, fps, (width, height))
                    
                    # 创建带有文字的帧
                    for frame_num in range(fps * duration):
                        # 创建一个纯色背景
                        img = np.zeros((height, width, 3), np.uint8)
                        
                        # 根据进度改变颜色
                        color_val = int(255 * (frame_num % fps) / fps)
                        img[:] = [color_val, 255 - color_val, 128]  # RGB
                        
                        # 添加文字
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        text = f"{title}"
                        font_scale = 1
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
                    print(f"成功创建视频文件: {video_filename}")
                except Exception as e:
                    print(f"创建视频文件时出错: {str(e)}, 使用虚拟文件")
                    # 如果OpenCV不可用，创建虚拟文件
                    with open(video_path, 'w') as f:
                        f.write(f"Virtual video file for {title}")
                
                # 生成唯一的缩略图文件名
                thumb_filename = f"local_thumb_{i+1}_{int(datetime.now().timestamp())}.jpg"
                thumb_path = os.path.join(videos_dir, thumb_filename)
                
                # 创建缩略图
                try:
                    # 创建一个有吸引力的缩略图
                    img = Image.new('RGB', (400, 300), color=(73, 109, 137))
                    d = ImageDraw.Draw(img)
                    
                    # 绘制渐变背景
                    for y in range(300):
                        r = int(73 + (182-73) * y / 300)
                        g = int(109 + (137-109) * y / 300)
                        b = int(137 + (204-137) * y / 300)
                        d.line([(0, y), (400, y)], fill=(r, g, b))
                    
                    # 添加文本
                    try:
                        # 尝试使用系统字体
                        from PIL import ImageFont
                        font = ImageFont.load_default()
                    except:
                        font = None
                    
                    # 主标题
                    title_lines = [title[j:j+10] for j in range(0, len(title), 10)]  # 每行最多10个字符
                    y_offset = 100
                    for line in title_lines:
                        bbox = d.textbbox((0, 0), line, font=font)
                        text_width = bbox[2] - bbox[0]
                        x = (400 - text_width) // 2
                        d.text((x, y_offset), line, fill=(255, 255, 255), font=font)
                        y_offset += 25
                    
                    # 添加播放图标
                    d.polygon([(150, 130), (150, 170), (180, 150)], fill=(255, 255, 255, 128))
                    
                    img.save(thumb_path)
                    print(f"成功创建缩略图: {thumb_filename}")
                except Exception as e:
                    print(f"创建缩略图时出错: {str(e)}, 使用虚拟文件")
                    # 如果PIL不可用，创建虚拟文件
                    with open(thumb_path, 'w') as f:
                        f.write(f"Virtual thumbnail for {title}")
                
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
        
        db.session.commit()
        print("本地视频和缩略图创建完成，数据库已更新")


if __name__ == '__main__':
    create_local_video_thumbnails()