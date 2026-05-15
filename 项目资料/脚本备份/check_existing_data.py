'''
Author: your name
Date: 2026-01-19 03:57:54
LastEditTime: 2026-01-19 03:57:55
LastEditors: your name
Description: In User Settings Edit
FilePath: \Q文件\python_web_project\check_existing_data.py
'''
import sqlite3

conn = sqlite3.connect('app.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print('数据库中的所有表:', tables)

# 检查用户表
cursor.execute('SELECT COUNT(*) FROM users;')
user_count = cursor.fetchone()[0]
print(f'用户数量: {user_count}')

# 检查视频表
cursor.execute('SELECT COUNT(*) FROM videos;')
video_count = cursor.fetchone()[0]
print(f'视频数量: {video_count}')

# 检查消息表
cursor.execute('SELECT COUNT(*) FROM messages;')
message_count = cursor.fetchone()[0]
print(f'消息数量: {message_count}')

# 检查新闻表
cursor.execute('SELECT COUNT(*) FROM news;')
news_count = cursor.fetchone()[0]
print(f'新闻数量: {news_count}')

# 检查帖子表
cursor.execute('SELECT COUNT(*) FROM posts;')
post_count = cursor.fetchone()[0]
print(f'帖子数量: {post_count}')

# 如果有用户，显示一些用户信息
if user_count > 0:
    cursor.execute('SELECT id, username, email FROM users LIMIT 5;')
    users = cursor.fetchall()
    print('前5个用户:', users)

conn.close()