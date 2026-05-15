'''
Author: your name
Date: 2026-01-19 03:50:22
LastEditTime: 2026-01-19 03:50:22
LastEditors: your name
Description: In User Settings Edit
FilePath: \Q文件\python_web_project\test_db_creation.py
'''
from app import app, db
from models import User, Post, Video, Comment, Message, News, PostLike, VideoLike, NewsLike, Trending, Follows, UserStatus
import os

print('检查数据库文件...')
if os.path.exists('app.db'):
    print('app.db存在')
else:
    print('app.db不存在，开始创建...')

with app.app_context():
    # 检查模型类是否定义正确
    print('检查模型定义...')
    print(f'User: {User}')
    print(f'News: {News}')
    print(f'Comment: {Comment}')
    
    # 创建所有表
    print('开始创建数据库表...')
    db.create_all()
    print('数据库表创建完成')

# 检查数据库文件和表
import sqlite3
conn = sqlite3.connect('app.db')
cursor = conn.cursor()

# 检查所有表
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print('数据库中的表:', tables)

# 检查特定表
for table_name in ['users', 'news', 'comments']:
    print(f'\n检查表 {table_name} 的结构:')
    try:
        cursor.execute(f'PRAGMA table_info({table_name})')
        rows = cursor.fetchall()
        for row in rows:
            print(f'  {row}')
    except sqlite3.Error as e:
        print(f'  错误: {e}')

conn.close()