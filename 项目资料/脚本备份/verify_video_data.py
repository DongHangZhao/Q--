'''
Author: your name
Date: 2026-01-11 01:21:05
LastEditTime: 2026-01-11 01:21:05
LastEditors: your name
Description: In User Settings Edit
FilePath: \Q文件\python_web_project\verify_video_data.py
'''
# -*- coding: utf-8 -*-
"""
验证真实视频数据是否已正确添加到数据库
"""
from app import app, db
from models import Video, Comment, User


def verify_video_data():
    """验证视频数据"""
    with app.app_context():
        print("=== 视频数据验证 ===")
        total_videos = Video.query.count()
        total_comments = Comment.query.count()
        
        print(f"总视频数: {total_videos}")
        print(f"总评论数: {total_comments}")
        
        print("\n=== 每个用户的视频信息 ===")
        builtin_users = ['admin', 'tianmi', 'FallPetal', 'zhangsan', 'lisi', 'xiaoming', 'zhaoliu', 'wangwu', 'meimei']
        
        for username in builtin_users:
            user = User.query.filter_by(username=username).first()
            if user:
                videos = Video.query.filter_by(uploader_id=user.id).all()
                print(f"\n用户 {username}:")
                for video in videos:
                    print(f"  - 视频: {video.title}")
                    print(f"    描述: {video.description[:50]}...")
                    print(f"    链接: {video.video_url}")
                    print(f"    上传时间: {video.timestamp}")
                    print(f"    观看次数: {video.views}")
                    print(f"    点赞数: {video.likes_count}")
                    print(f"    评论数: {video.comments_count}")
                    
                    # 显示该视频的评论
                    comments = Comment.query.filter_by(video_id=video.id).all()
                    if comments:
                        print(f"    评论示例 (共{len(comments)}条):")
                        for i, comment in enumerate(comments[:2]):  # 只显示前2条评论
                            print(f"      {i+1}. {comment.content} (评论时间: {comment.timestamp})")
                    print()


if __name__ == '__main__':
    verify_video_data()