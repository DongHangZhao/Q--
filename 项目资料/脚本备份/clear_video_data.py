'''
Author: your name
Date: 2026-01-11 01:20:21
LastEditTime: 2026-01-11 01:20:21
LastEditors: your name
Description: In User Settings Edit
FilePath: \Q文件\python_web_project\clear_video_data.py
'''
# -*- coding: utf-8 -*-
"""
清除现有的视频数据，以便重新添加真实视频数据
"""
from app import app, db
from models import Video, Comment


def clear_video_data():
    """清除现有的视频和评论数据"""
    with app.app_context():
        # 删除所有评论（因为它们引用了视频）
        Comment.query.delete()
        
        # 删除所有视频
        Video.query.delete()
        
        db.session.commit()
        print("视频和评论数据已清除")


if __name__ == '__main__':
    clear_video_data()