'''
Author: your name
Date: 2026-01-11 02:44:54
LastEditTime: 2026-01-11 02:44:55
LastEditors: your name
Description: In User Settings Edit
FilePath: \Q文件\python_web_project\generate_video_thumbnails.py
'''
# -*- coding: utf-8 -*-
"""
从视频中随机提取帧作为封面图，并为新上传的视频自动设置封面
"""
import os
import cv2
import random
from PIL import Image
from app import app, db
from models import Video
import math


def extract_frame_as_thumbnail(video_path, output_path, frame_number=None):
    """
    从视频中提取指定帧作为缩略图
    
    Args:
        video_path: 视频文件路径
        output_path: 输出缩略图路径
        frame_number: 要提取的帧号，如果为None则随机选择
    """
    try:
        # 打开视频文件
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"无法打开视频文件: {video_path}")
            return False
        
        # 获取视频总帧数
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        if total_frames <= 0:
            print(f"视频文件无帧数据: {video_path}")
            cap.release()
            return False
        
        # 如果未指定帧号，则随机选择一个中间段的帧
        if frame_number is None:
            # 选择视频中间80%部分的随机帧，避免开头结尾的黑屏
            start_frame = int(total_frames * 0.1)
            end_frame = int(total_frames * 0.9)
            frame_number = random.randint(start_frame, end_frame)
        else:
            frame_number = min(frame_number, total_frames - 1)
        
        # 设置视频读取位置到指定帧
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        
        # 读取帧
        ret, frame = cap.read()
        if not ret:
            print(f"无法读取视频帧: {video_path}, 帧号: {frame_number}")
            cap.release()
            return False
        
        # 转换BGR到RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # 转换为PIL图像
        pil_image = Image.fromarray(frame_rgb)
        
        # 调整尺寸（保持原始宽高比，但限制最大尺寸）
        max_size = (400, 400)
        pil_image.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # 保存图像
        pil_image.save(output_path, 'JPEG', quality=85, optimize=True)
        
        cap.release()
        print(f"成功从视频 {video_path} 提取第 {frame_number} 帧作为缩略图: {output_path}")
        return True
    except Exception as e:
        print(f"提取缩略图时出错 {video_path}: {str(e)}")
        return False


def update_existing_video_thumbnails():
    """为现有视频更新缩略图，从视频中提取帧作为封面"""
    with app.app_context():
        videos = Video.query.all()
        
        for video in videos:
            # 获取视频文件完整路径
            video_file_path = os.path.join('static', video.video_url)
            
            if not os.path.exists(video_file_path):
                print(f"视频文件不存在: {video_file_path}")
                continue
            
            # 生成新的缩略图文件名
            video_dir = os.path.dirname(video_file_path)
            video_filename = os.path.splitext(os.path.basename(video_file_path))[0]
            new_thumb_filename = f"{video_filename}_thumb.jpg"
            new_thumb_path = os.path.join(video_dir, new_thumb_filename)
            
            # 提取帧作为缩略图
            if extract_frame_as_thumbnail(video_file_path, new_thumb_path):
                # 更新数据库中的缩略图路径
                relative_path = os.path.join(os.path.dirname(video.video_url), new_thumb_filename)
                video.thumbnail_url = relative_path
                db.session.commit()
                print(f"视频 '{video.title}' 的缩略图已更新为: {relative_path}")
            else:
                print(f"为视频 '{video.title}' 生成缩略图失败")


def auto_generate_thumbnail_for_video(video_id):
    """
    为指定视频自动生成缩略图
    
    Args:
        video_id: 视频ID
    """
    with app.app_context():
        video = Video.query.get(video_id)
        if not video:
            print(f"未找到视频ID: {video_id}")
            return False
        
        # 获取视频文件完整路径
        video_file_path = os.path.join('static', video.video_url)
        
        if not os.path.exists(video_file_path):
            print(f"视频文件不存在: {video_file_path}")
            return False
        
        # 生成新的缩略图文件名
        video_dir = os.path.dirname(video_file_path)
        video_filename = os.path.splitext(os.path.basename(video_file_path))[0]
        new_thumb_filename = f"{video_filename}_thumb.jpg"
        new_thumb_path = os.path.join(video_dir, new_thumb_filename)
        
        # 提取帧作为缩略图
        if extract_frame_as_thumbnail(video_file_path, new_thumb_path):
            # 更新数据库中的缩略图路径
            relative_path = os.path.join(os.path.dirname(video.video_url), new_thumb_filename)
            video.thumbnail_url = relative_path
            db.session.commit()
            print(f"视频 '{video.title}' 的缩略图已自动生成: {relative_path}")
            return True
        else:
            print(f"为视频 '{video.title}' 自动生成缩略图失败")
            return False


def batch_generate_thumbnails(video_ids=None):
    """
    批量为视频生成缩略图
    
    Args:
        video_ids: 要处理的视频ID列表，如果为None则处理所有视频
    """
    with app.app_context():
        if video_ids:
            videos = Video.query.filter(Video.id.in_(video_ids)).all()
        else:
            videos = Video.query.all()
        
        success_count = 0
        fail_count = 0
        
        for video in videos:
            # 获取视频文件完整路径
            video_file_path = os.path.join('static', video.video_url)
            
            if not os.path.exists(video_file_path):
                print(f"视频文件不存在: {video_file_path}")
                fail_count += 1
                continue
            
            # 生成新的缩略图文件名
            video_dir = os.path.dirname(video_file_path)
            video_filename = os.path.splitext(os.path.basename(video_file_path))[0]
            new_thumb_filename = f"{video_filename}_auto_thumb.jpg"
            new_thumb_path = os.path.join(video_dir, new_thumb_filename)
            
            # 提取帧作为缩略图
            if extract_frame_as_thumbnail(video_file_path, new_thumb_path):
                # 更新数据库中的缩略图路径
                relative_path = os.path.join(os.path.dirname(video.video_url), new_thumb_filename)
                video.thumbnail_url = relative_path
                success_count += 1
                print(f"视频 '{video.title}' 的缩略图已自动生成: {relative_path}")
            else:
                fail_count += 1
                print(f"为视频 '{video.title}' 自动生成缩略图失败")
        
        db.session.commit()
        print(f"批量生成缩略图完成: 成功 {success_count} 个, 失败 {fail_count} 个")
        return success_count, fail_count


if __name__ == '__main__':
    print("视频缩略图生成工具")
    print("1. 为所有现有视频更新缩略图")
    print("2. 为指定视频ID生成缩略图")
    print("3. 批量生成缩略图")
    
    choice = input("请选择操作 (1/2/3): ")
    
    if choice == '1':
        update_existing_video_thumbnails()
    elif choice == '2':
        video_id = int(input("请输入视频ID: "))
        auto_generate_thumbnail_for_video(video_id)
    elif choice == '3':
        video_ids_input = input("请输入视频ID列表(用逗号分隔，留空处理所有视频): ")
        if video_ids_input.strip():
            video_ids = [int(id.strip()) for id in video_ids_input.split(',')]
            batch_generate_thumbnails(video_ids)
        else:
            batch_generate_thumbnails()
    else:
        print("无效选择")