# -*- coding: utf-8 -*-
"""
更新视频的评论计数
"""
from app import app, db
from models import Video, Comment


def update_video_counts():
    """更新视频的评论计数"""
    with app.app_context():
        videos = Video.query.all()
        for video in videos:
            comment_count = Comment.query.filter_by(video_id=video.id).count()
            video.comments_count = comment_count
            print(f"更新视频 '{video.title}' 的评论计数为: {comment_count}")
        
        db.session.commit()
        print("视频评论计数更新完成")


if __name__ == '__main__':
    update_video_counts()