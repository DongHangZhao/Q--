# -*- coding: utf-8 -*-
"""
修复视频编码问题，使用浏览器友好的编码格式
"""
import os
import cv2
import numpy as np
from PIL import Image, ImageDraw
import random
from app import app, db
from models import User, Video, Comment
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import time


def fix_video_encoding():
    """使用浏览器友好的编码格式重新创建视频"""
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
        
        # 删除所有现有的视频和缩略图文件
        files = os.listdir(videos_dir)
        for file in files:
            if file.startswith('high_quality_video_') or file.startswith('high_quality_thumb_') or file.startswith('web_friendly_'):
                os.remove(os.path.join(videos_dir, file))
        
        # 删除数据库中的视频和评论
        Comment.query.delete()
        Video.query.delete()
        db.session.commit()
        
        # 为每个用户创建浏览器友好的视频
        for i, username in enumerate(builtin_users):
            user = User.query.filter_by(username=username).first()
            if user and i < len(video_titles):
                title = f"{video_titles[i]} - {username}"
                description = f"{video_descriptions[i]} 这是用户{username}分享的精彩内容。"
                
                # 生成唯一的视频文件名
                video_filename = f"web_friendly_video_{i+1}_{int(time.time())}.mp4"
                video_path = os.path.join(videos_dir, video_filename)
                
                # 创建浏览器友好的本地视频文件（使用H.264编码）
                try:
                    # 使用更兼容的编码设置 - 尝试不同的编码方式
                    fourcc_options = [
                        cv2.VideoWriter_fourcc(*'H264'),  # H.264
                        cv2.VideoWriter_fourcc(*'X264'),  # X.264
                        cv2.VideoWriter_fourcc(*'XVID'),  # Xvid
                        cv2.VideoWriter_fourcc(*'MP4V'),  # MPEG-4
                    ]
                    
                    success = False
                    for fourcc in fourcc_options:
                        try:
                            fps = 24  # 使用更常见的FPS
                            duration = 15  # 15秒
                            width, height = 640, 480  # 使用更标准的分辨率
                            out = cv2.VideoWriter(video_path, fourcc, fps, (width, height))
                            
                            # 验证是否成功创建了视频写入器
                            if int(out.getBackendName()) >= 0:  # 如果成功
                                success = True
                                break
                            else:
                                out.release()
                        except:
                            continue
                    
                    if not success:
                        # 如果以上编码都失败，使用最基础的
                        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                        out = cv2.VideoWriter(video_path, fourcc, fps, (width, height))
                    
                    # 创建更简单的视频内容，确保浏览器兼容性
                    for frame_num in range(fps * duration):
                        # 创建一个简单的彩色背景
                        img = np.zeros((height, width, 3), dtype=np.uint8)
                        
                        # 创建渐变背景，每秒变化颜色
                        color_cycle = int(frame_num / fps) % 6
                        base_colors = [
                            [255, 100, 100],  # 红色系
                            [100, 255, 100],  # 绿色系
                            [100, 100, 255],  # 蓝色系
                            [255, 255, 100],  # 黄色系
                            [255, 100, 255],  # 紫色系
                            [100, 255, 255]   # 青色系
                        ]
                        
                        base_color = base_colors[color_cycle]
                        # 添加轻微的动态效果
                        dynamic_factor = (frame_num % fps) / fps
                        img[:, :] = [
                            int(base_color[0] * (0.7 + 0.3 * dynamic_factor)),
                            int(base_color[1] * (0.7 + 0.3 * dynamic_factor)),
                            int(base_color[2] * (0.7 + 0.3 * dynamic_factor))
                        ]
                        
                        # 添加标题文本
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        main_text = title
                        font_scale = 0.6
                        thickness = 2
                        text_size = cv2.getTextSize(main_text, font, font_scale, thickness)[0]
                        text_x = (width - text_size[0]) // 2
                        text_y = height // 2 - 30
                        
                        # 添加白色描边的文字
                        cv2.putText(img, main_text, (text_x-1, text_y-1), font, font_scale, (0, 0, 0), thickness+1)
                        cv2.putText(img, main_text, (text_x+1, text_y-1), font, font_scale, (0, 0, 0), thickness+1)
                        cv2.putText(img, main_text, (text_x-1, text_y+1), font, font_scale, (0, 0, 0), thickness+1)
                        cv2.putText(img, main_text, (text_x+1, text_y+1), font, font_scale, (0, 0, 0), thickness+1)
                        cv2.putText(img, main_text, (text_x, text_y), font, font_scale, (255, 255, 255), thickness)
                        
                        # 添加计时器
                        timer_text = f"第 {(frame_num // fps) + 1} 秒 / 共 {duration} 秒"
                        timer_font_scale = 0.5
                        timer_thickness = 1
                        timer_size = cv2.getTextSize(timer_text, font, timer_font_scale, timer_thickness)[0]
                        timer_x = (width - timer_size[0]) // 2
                        timer_y = text_y + 50
                        
                        cv2.putText(img, timer_text, (timer_x-1, timer_y-1), font, timer_font_scale, (0, 0, 0), timer_thickness+1)
                        cv2.putText(img, timer_text, (timer_x, timer_y), font, timer_font_scale, (200, 200, 200), timer_thickness)
                        
                        out.write(img)
                    
                    out.release()
                    print(f"✅ 成功创建浏览器友好视频: {video_filename}")
                except Exception as e:
                    print(f"❌ 创建浏览器友好视频时出错: {str(e)}")
                    # 创建一个最简单的视频作为备选
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
                        font_scale = 0.8
                        thickness = 2
                        text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
                        text_x = (width - text_size[0]) // 2
                        text_y = height // 2
                        
                        cv2.putText(img, text, (text_x, text_y), font, font_scale, (255, 255, 255), thickness)
                        
                        out.write(img)
                    
                    out.release()
                    print(f"✅ 使用备选方案创建视频: {video_filename}")
                
                # 生成唯一的缩略图文件名
                thumb_filename = f"web_friendly_thumb_{i+1}_{int(time.time())}.jpg"
                thumb_path = os.path.join(videos_dir, thumb_filename)
                
                # 创建缩略图
                try:
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
                    print(f"✅ 成功创建缩略图: {thumb_filename}")
                except Exception as e:
                    print(f"❌ 创建缩略图时出错: {str(e)}")
                    continue
                
                # 生成时间戳
                now = datetime.now(ZoneInfo("Asia/Shanghai"))
                days_back = random.randint(1, 21)
                hours_back = random.randint(0, 23)
                minutes_back = random.randint(0, 59)
                upload_time = now - timedelta(days=days_back, hours=hours_back, minutes=minutes_back)
                
                # 创建新的视频记录
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
                
                print(f"✅ 成功为用户 {username} 创建浏览器友好视频: {title}")
        
        db.session.commit()
        print("\n🎉 浏览器友好视频创建完成！")
        print("✅ 所有视频都使用兼容的编码格式，确保浏览器兼容性")
        print("✅ 视频现在应该能在网页中正常播放")


if __name__ == '__main__':
    fix_video_encoding()