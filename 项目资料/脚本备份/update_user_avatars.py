'''
Author: your name
Date: 2026-01-10 15:16:27
LastEditTime: 2026-01-10 15:16:27
LastEditors: your name
Description: In User Settings Edit
FilePath: \Q文件\python_web_project\update_user_avatars.py
'''
"""
为所有用户初始化网络头像
"""

from app import app, db
from models import User
import random

# 网络头像URL列表
AVATAR_URLS = [
    "https://picsum.photos/200/200?random=1",
    "https://picsum.photos/200/200?random=2", 
    "https://picsum.photos/200/200?random=3",
    "https://picsum.photos/200/200?random=4",
    "https://picsum.photos/200/200?random=5",
    "https://picsum.photos/200/200?random=6",
    "https://picsum.photos/200/200?random=7",
    "https://picsum.photos/200/200?random=8",
    "https://picsum.photos/200/200?random=9",
    "https://picsum.photos/200/200?random=10",
    "https://picsum.photos/200/200?random=11",
    "https://picsum.photos/200/200?random=12",
    "https://picsum.photos/200/200?random=13",
    "https://picsum.photos/200/200?random=14",
    "https://picsum.photos/200/200?random=15",
    "https://picsum.photos/200/200?random=16",
    "https://picsum.photos/200/200?random=17",
    "https://picsum.photos/200/200?random=18",
    "https://picsum.photos/200/200?random=19",
    "https://picsum.photos/200/200?random=20",
]

def update_user_avatars():
    with app.app_context():
        users = User.query.all()
        for i, user in enumerate(users):
            # 为每个用户分配一个随机头像
            user.avatar = AVATAR_URLS[i % len(AVATAR_URLS)]
        
        db.session.commit()
        print(f"更新了 {len(users)} 个用户的头像")

if __name__ == "__main__":
    update_user_avatars()