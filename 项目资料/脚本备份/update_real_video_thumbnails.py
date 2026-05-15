"""
更新数据库中真实视频的缩略图路径
"""
from app import app, db
from models import Video
import os


def update_real_video_thumbnails():
    """更新真实视频的缩略图路径"""
    with app.app_context():
        # 获取所有真实视频（标题包含特定关键词的视频）
        real_videos = Video.query.filter(
            Video.video_url.like('%real_video%')
        ).all()
        
        print(f"找到 {len(real_videos)} 个真实视频:")
        
        updated_count = 0
        for video in real_videos:
            # 获取视频文件名（不含路径）
            video_filename = os.path.basename(video.video_url)
            video_basename = os.path.splitext(video_filename)[0]
            
            # 构造新的缩略图文件名
            new_thumb_filename = f"{video_basename}_auto_thumb.jpg"
            new_thumb_path = os.path.join('static', 'uploads', 'videos', new_thumb_filename)
            
            # 检查新缩略图是否存在
            if os.path.exists(new_thumb_path):
                # 更新数据库中的缩略图路径
                video.thumbnail_url = f"uploads/videos/{new_thumb_filename}"
                print(f"  - 更新视频 '{video.title}': {video.thumbnail_url}")
                updated_count += 1
            else:
                print(f"  - 未找到缩略图文件: {new_thumb_path}")
        
        # 提交更改
        db.session.commit()
        print(f"\n成功更新了 {updated_count} 个视频的缩略图路径")


if __name__ == '__main__':
    update_real_video_thumbnails()