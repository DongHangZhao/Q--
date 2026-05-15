'''
Author: your name
Date: 2026-01-11 01:37:18
LastEditTime: 2026-01-11 01:37:19
LastEditors: your name
Description: In User Settings Edit
FilePath: \Q文件\python_web_project\create_high_quality_videos.py
'''
# -*- coding: utf-8 -*-
"""
创建高质量的本地短视频和封面图，确保可以正常播放
"""
import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import random
from app import app, db
from models import User, Video, Comment
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import time


def create_high_quality_videos():
    """创建高质量的本地短视频和封面图"""
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
        
        # 为每个用户创建高质量的视频和封面
        for i, username in enumerate(builtin_users):
            user = User.query.filter_by(username=username).first()
            if user:
                title = f"{video_titles[i]} - {username}"
                description = f"{video_descriptions[i]} 这是用户{username}分享的精彩内容。"
                
                # 生成唯一的视频文件名
                video_filename = f"high_quality_video_{i+1}_{int(time.time())}.mp4"
                video_path = os.path.join(videos_dir, video_filename)
                
                # 创建高质量的本地视频文件
                try:
                    # 设置视频参数
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 使用mp4v编码
                    fps = 30
                    duration = 15  # 15秒
                    width, height = 720, 1280  # 竖屏比例，更适合短视频
                    out = cv2.VideoWriter(video_path, fourcc, fps, (width, height))
                    
                    # 创建更丰富的视频内容
                    for frame_num in range(fps * duration):
                        # 创建一个渐变背景
                        img = np.zeros((height, width, 3), dtype=np.uint8)
                        
                        # 创建动态渐变效果
                        for y in range(height):
                            # 计算颜色值，随时间和位置变化
                            r = int(50 + 100 * (np.sin(frame_num * 0.1 + y * 0.01) + 1) / 2)
                            g = int(80 + 120 * (np.cos(frame_num * 0.1 + y * 0.01) + 1) / 2)
                            b = int(100 + 100 * (np.sin(frame_num * 0.05 + y * 0.02) + 1) / 2)
                            img[y, :] = [b, g, r]  # OpenCV使用BGR顺序
                        
                        # 添加主标题
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        main_text = title
                        font_scale = 1.2
                        thickness = 3
                        text_size = cv2.getTextSize(main_text, font, font_scale, thickness)[0]
                        text_x = (width - text_size[0]) // 2
                        text_y = height // 2 - 50
                        
                        # 添加阴影效果
                        cv2.putText(img, main_text, (text_x+2, text_y+2), font, font_scale, (0, 0, 0), thickness+2)
                        cv2.putText(img, main_text, (text_x, text_y), font, font_scale, (255, 255, 255), thickness)
                        
                        # 添加副标题
                        sub_text = f"第 {(frame_num // fps) + 1} 秒 / 共 {duration} 秒"
                        sub_font_scale = 0.8
                        sub_thickness = 2
                        sub_text_size = cv2.getTextSize(sub_text, font, sub_font_scale, sub_thickness)[0]
                        sub_text_x = (width - sub_text_size[0]) // 2
                        sub_text_y = text_y + 80
                        
                        cv2.putText(img, sub_text, (sub_text_x+1, sub_text_y+1), font, sub_font_scale, (0, 0, 0), sub_thickness+1)
                        cv2.putText(img, sub_text, (sub_text_x, sub_text_y), font, sub_font_scale, (200, 200, 200), sub_thickness)
                        
                        # 添加装饰元素
                        # 添加圆形装饰
                        center_x, center_y = width // 2, height // 2 - 100
                        radius = int(30 + 20 * np.sin(frame_num * 0.05))
                        color = (255, 255, 255)
                        cv2.circle(img, (center_x, center_y), radius, color, 2)
                        
                        # 添加移动的点
                        point_x = int(width * 0.1 + 0.8 * width * (frame_num % fps) / fps)
                        point_y = int(height * 0.8)
                        cv2.circle(img, (point_x, point_y), 10, (255, 255, 0), -1)
                        
                        out.write(img)
                    
                    out.release()
                    print(f"✅ 成功创建高质量视频: {video_filename}")
                except Exception as e:
                    print(f"❌ 创建视频文件时出错: {str(e)}, 回退到简单视频")
                    # 如果高级视频创建失败，创建一个简单的视频
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                    fps = 24
                    duration = 10
                    width, height = 640, 480
                    out = cv2.VideoWriter(video_path, fourcc, fps, (width, height))
                    
                    for frame_num in range(fps * duration):
                        img = np.zeros((height, width, 3), np.uint8)
                        color_val = int(100 + 100 * (frame_num % fps) / fps)
                        img[:] = [max(0, 200 - color_val), min(255, color_val), 150]
                        
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        text = title
                        font_scale = 1
                        thickness = 2
                        text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
                        text_x = (width - text_size[0]) // 2
                        text_y = height // 2
                        
                        cv2.putText(img, text, (text_x, text_y), font, font_scale, (255, 255, 255), thickness)
                        out.write(img)
                    
                    out.release()
                
                # 生成唯一的缩略图文件名
                thumb_filename = f"high_quality_thumb_{i+1}_{int(time.time())}.jpg"
                thumb_path = os.path.join(videos_dir, thumb_filename)
                
                # 创建高质量的缩略图
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
                    
                    # 添加标题文本，支持中文
                    try:
                        # 尝试使用系统字体来支持中文
                        font = ImageFont.truetype("arial.ttf", 16)  # Windows系统字体
                    except:
                        try:
                            font = ImageFont.truetype("simhei.ttf", 16)  # 黑体，常见中文字体
                        except:
                            try:
                                font = ImageFont.truetype("msyh.ttc", 16)  # 微软雅黑
                            except:
                                font = ImageFont.load_default()  # 回退到默认字体
                    
                    # 分行显示标题
                    title_lines = [title[j:j+12] for j in range(0, len(title), 12)]  # 每行最多12个字符
                    y_offset = 100
                    for line in title_lines:
                        try:
                            # 使用文本边界框来计算文本尺寸
                            bbox = d.textbbox((0, 0), line, font=font)
                            text_width = bbox[2] - bbox[0]
                            text_height = bbox[3] - bbox[1]
                            x = (400 - text_width) // 2
                            d.text((x, y_offset), line, fill=(255, 255, 255), font=font)
                        except:
                            # 如果字体不支持中文，则使用默认方式
                            text_width, text_height = d.textsize(line) if hasattr(d, 'textsize') else (100, 20)
                            x = (400 - text_width) // 2
                            d.text((x, y_offset), line, fill=(255, 255, 255), font=font)
                        
                        y_offset += text_height + 5
                    
                    # 添加播放图标
                    d.polygon([(150, 180), (150, 220), (190, 200)], fill=(255, 255, 255, 200))
                    
                    # 添加用户名称
                    try:
                        user_bbox = d.textbbox((0, 0), username, font=font)
                        user_width = user_bbox[2] - user_bbox[0]
                        d.text(((400 - user_width) // 2, 250), username, fill=(200, 200, 200), font=font)
                    except:
                        user_width = d.textsize(username)[0] if hasattr(d, 'textsize') else 60
                        d.text(((400 - user_width) // 2, 250), username, fill=(200, 200, 200), font=font)
                    
                    img.save(thumb_path, quality=95)  # 高质量保存
                    print(f"✅ 成功创建高质量缩略图: {thumb_filename}")
                except Exception as e:
                    print(f"❌ 创建缩略图时出错: {str(e)}, 使用简单缩略图")
                    # 如果高级缩略图创建失败，创建一个简单的缩略图
                    img = Image.new('RGB', (400, 300), color=(73, 109, 137))
                    d = ImageDraw.Draw(img)
                    
                    # 绘制基本背景和文本
                    try:
                        font = ImageFont.load_default()
                    except:
                        font = None
                    
                    # 主标题
                    title_lines = [title[j:j+10] for j in range(0, len(title), 10)]
                    y_offset = 100
                    for line in title_lines:
                        d.text((50, y_offset), line, fill=(255, 255, 255), font=font)
                        y_offset += 25
                    
                    # 添加播放图标
                    d.polygon([(150, 130), (150, 170), (180, 150)], fill=(255, 255, 255, 128))
                    
                    img.save(thumb_path)
                
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
                
                print(f"✅ 成功为用户 {username} 创建高质量视频: {title} (本地文件: {video_filename})，包含 {num_comments} 条评论")
        
        db.session.commit()
        print("\n🎉 高质量视频和缩略图创建完成！")
        print("✅ 所有视频都使用本地生成的MP4文件，确保可以正常播放")
        print("✅ 所有缩略图都使用本地生成的JPG文件，确保可以正常显示")
        print("✅ 数据库已更新，包含了正确的文件路径")


if __name__ == '__main__':
    create_high_quality_videos()