'''
Author: your name
Date: 2026-01-19 04:21:01
LastEditTime: 2026-01-19 04:21:01
LastEditors: your name
Description: In User Settings Edit
FilePath: \Q文件\python_web_project\db_check.py
'''
import sqlite3

# 连接到数据库
conn = sqlite3.connect('app.db')
cursor = conn.cursor()

print('=== 数据库状态检查 ===')
print('数据库文件: app.db')
print()

# 检查所有表
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print('所有表:', [table[0] for table in tables])
print()

# 检查用户表
print('=== 用户信息 ===')
cursor.execute('SELECT id, username, email, join_date FROM users ORDER BY id;')
users = cursor.fetchall()
print(f'用户总数: {len(users)}')
for user in users:
    print(f'  ID: {user[0]}, Username: {user[1]}, Email: {user[2]}, 注册时间: {user[3]}')
print()

# 检查关注关系
print('=== 关注关系 ===')
cursor.execute('SELECT COUNT(*) FROM follows;')
follows_count = cursor.fetchone()[0]
print(f'关注关系数量: {follows_count}')
if follows_count > 0:
    cursor.execute('SELECT follower_id, followed_id FROM follows;')
    follows = cursor.fetchall()
    for follow in follows[:10]:  # 显示前10个
        print(f'  用户{follow[0]} -> 用户{follow[1]}')
print()

# 检查帖子
print('=== 帖子信息 ===')
cursor.execute('SELECT COUNT(*) FROM posts;')
posts_count = cursor.fetchone()[0]
print(f'帖子数量: {posts_count}')
if posts_count > 0:
    cursor.execute('SELECT id, title, author_id FROM posts;')
    posts = cursor.fetchall()
    for post in posts[:5]:  # 显示前5个
        print(f'  ID: {post[0]}, 标题: {post[1][:30]}..., 作者ID: {post[2]}')
print()

# 检查视频
print('=== 视频信息 ===')
cursor.execute('SELECT COUNT(*) FROM videos;')
videos_count = cursor.fetchone()[0]
print(f'视频数量: {videos_count}')
if videos_count > 0:
    cursor.execute('SELECT id, title, uploader_id FROM videos;')
    videos = cursor.fetchall()
    for video in videos[:5]:  # 显示前5个
        print(f'  ID: {video[0]}, 标题: {video[1][:30]}..., 上传者ID: {video[2]}')
print()

# 检查新闻
print('=== 新闻信息 ===')
cursor.execute('SELECT COUNT(*) FROM news;')
news_count = cursor.fetchone()[0]
print(f'新闻数量: {news_count}')
if news_count > 0:
    cursor.execute('SELECT id, title FROM news;')
    news = cursor.fetchall()
    for item in news[:5]:  # 显示前5个
        print(f'  ID: {item[0]}, 标题: {item[1][:50]}...')
print()

# 检查消息
print('=== 消息信息 ===')
cursor.execute('SELECT COUNT(*) FROM messages;')
messages_count = cursor.fetchone()[0]
print(f'消息数量: {messages_count}')
if messages_count > 0:
    cursor.execute('SELECT id, sender_id, recipient_id, content FROM messages;')
    messages = cursor.fetchall()
    for msg in messages[:5]:  # 显示前5个
        print(f'  ID: {msg[0]}, 发送者: {msg[1]}, 接收者: {msg[2]}, 内容: {msg[3][:50]}...')
print()

# 检查评论
print('=== 评论信息 ===')
cursor.execute('SELECT COUNT(*) FROM comments;')
comments_count = cursor.fetchone()[0]
print(f'评论数量: {comments_count}')
if comments_count > 0:
    cursor.execute('SELECT id, author_id, content FROM comments;')
    comments = cursor.fetchall()
    for comment in comments[:5]:  # 显示前5个
        print(f'  ID: {comment[0]}, 作者ID: {comment[1]}, 内容: {comment[2][:50]}...')

conn.close()