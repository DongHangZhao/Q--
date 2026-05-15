"""
更新现有视频和新闻的缩略图和图片为真实的网络图片
"""

from app import app, db
from models import Video, News

# 真实的网络图片URL列表
VIDEO_THUMBNAILS = [
    "https://picsum.photos/400/225?random=1",
    "https://picsum.photos/400/225?random=2",
    "https://picsum.photos/400/225?random=3",
    "https://picsum.photos/400/225?random=4",
    "https://picsum.photos/400/225?random=5",
    "https://picsum.photos/400/225?random=6",
    "https://picsum.photos/400/225?random=7",
    "https://picsum.photos/400/225?random=8",
    "https://picsum.photos/400/225?random=9",
    "https://picsum.photos/400/225?random=10",
]

NEWS_IMAGES = [
    "https://picsum.photos/400/250?random=11",
    "https://picsum.photos/400/250?random=12",
    "https://picsum.photos/400/250?random=13",
    "https://picsum.photos/400/250?random=14",
    "https://picsum.photos/400/250?random=15",
    "https://picsum.photos/400/250?random=16",
    "https://picsum.photos/400/250?random=17",
    "https://picsum.photos/400/250?random=18",
    "https://picsum.photos/400/250?random=19",
    "https://picsum.photos/400/250?random=20",
]

def update_thumbnails():
    with app.app_context():
        # 更新视频缩略图
        videos = Video.query.all()
        for i, video in enumerate(videos):
            if not video.thumbnail_url or not video.thumbnail_url.startswith('http'):
                video.thumbnail_url = VIDEO_THUMBNAILS[i % len(VIDEO_THUMBNAILS)]
        
        # 更新新闻图片
        news_items = News.query.all()
        for i, news_item in enumerate(news_items):
            if not news_item.image_url or not news_item.image_url.startswith('http'):
                news_item.image_url = NEWS_IMAGES[i % len(NEWS_IMAGES)]
        
        db.session.commit()
        print(f"更新了 {len(videos)} 个视频的缩略图")
        print(f"更新了 {len(news_items)} 个新闻的图片")

if __name__ == "__main__":
    update_thumbnails()