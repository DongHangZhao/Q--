'''
Author: your name
Date: 2026-01-19 04:24:09
LastEditTime: 2026-01-19 04:24:09
LastEditors: your name
Description: In User Settings Edit
FilePath: \Q文件\python_web_project\merge_databases.py
'''
import sqlite3
from datetime import datetime

def merge_databases():
    # 连接两个数据库
    original_conn = sqlite3.connect('database/users.db')
    main_conn = sqlite3.connect('app.db')
    
    original_cursor = original_conn.cursor()
    main_cursor = main_conn.cursor()
    
    print("开始合并数据库...")
    
    # 从原始数据库复制用户数据
    print("复制用户数据...")
    original_cursor.execute("SELECT * FROM users;")
    original_users = original_cursor.fetchall()
    
    main_cursor.execute("SELECT * FROM users;")
    main_users = main_cursor.fetchall()
    
    print(f"原始数据库用户数: {len(original_users)}")
    print(f"主数据库用户数: {len(main_users)}")
    
    # 复制原始数据库的用户（跳过已存在的）
    for user in original_users:
        user_id, username, email, password_hash, avatar, bio, location, website, is_active, is_banned, can_post, can_video, can_comment, is_admin, join_date, last_seen = user
        
        # 检查用户是否已存在于主数据库中
        main_cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?", (username, email))
        existing_user = main_cursor.fetchone()
        
        if not existing_user:
            try:
                main_cursor.execute("""
                    INSERT OR REPLACE INTO users 
                    (id, username, email, password_hash, avatar, bio, location, website, 
                     is_active, is_banned, can_post, can_video, can_comment, is_admin, join_date, last_seen)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, user)
                print(f"  添加用户: {username}")
            except sqlite3.IntegrityError as e:
                print(f"  跳过用户 {username} (可能ID冲突): {e}")
    
    # 复制消息数据
    print("复制消息数据...")
    original_cursor.execute("SELECT * FROM messages;")
    original_messages = original_cursor.fetchall()
    
    main_cursor.execute("SELECT COUNT(*) FROM messages;")
    main_messages_count = main_cursor.fetchone()[0]
    
    print(f"原始数据库消息数: {len(original_messages)}")
    print(f"主数据库消息数: {main_messages_count}")
    
    for msg in original_messages:
        msg_id, sender_id, recipient_id, content, timestamp, is_read, msg_type, related_id, related_type, attachment_path, attachment_type, attachment_filename = msg
        
        # 检查消息是否已存在
        main_cursor.execute("SELECT id FROM messages WHERE content = ? AND sender_id = ? AND recipient_id = ? AND timestamp = ?", 
                           (content, sender_id, recipient_id, timestamp))
        existing_msg = main_cursor.fetchone()
        
        if not existing_msg:
            try:
                main_cursor.execute("""
                    INSERT OR IGNORE INTO messages
                    (id, sender_id, recipient_id, content, timestamp, is_read, message_type, 
                     related_id, related_type, attachment_path, attachment_type, attachment_filename)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (msg_id, sender_id, recipient_id, content, timestamp, is_read, msg_type, related_id, related_type, attachment_path, attachment_type, attachment_filename))
            except sqlite3.IntegrityError as e:
                print(f"  消息插入失败: {e}")
    
    # 复制关注关系
    print("复制关注关系...")
    original_cursor.execute("SELECT * FROM follows;")
    original_follows = original_cursor.fetchall()
    
    main_cursor.execute("SELECT COUNT(*) FROM follows;")
    main_follows_count = main_cursor.fetchone()[0]
    
    print(f"原始数据库关注关系数: {len(original_follows)}")
    print(f"主数据库关注关系数: {main_follows_count}")
    
    for follow in original_follows:
        follower_id, followed_id, timestamp = follow
        
        # 检查关注关系是否已存在
        main_cursor.execute("SELECT 1 FROM follows WHERE follower_id = ? AND followed_id = ?", (follower_id, followed_id))
        existing_follow = main_cursor.fetchone()
        
        if not existing_follow:
            try:
                main_cursor.execute("INSERT OR IGNORE INTO follows (follower_id, followed_id, timestamp) VALUES (?, ?, ?)", 
                                   (follower_id, followed_id, timestamp))
            except sqlite3.IntegrityError as e:
                print(f"  关注关系插入失败: {e}")
    
    # 复制帖子数据
    print("复制帖子数据...")
    original_cursor.execute("SELECT * FROM posts;")
    original_posts = original_cursor.fetchall()
    
    for post in original_posts:
        post_id, title, content, image_url, video_url, timestamp, updated_at, author_id, likes_count, comments_count = post
        
        # 检查帖子是否已存在
        main_cursor.execute("SELECT id FROM posts WHERE title = ? AND author_id = ?", (title, author_id))
        existing_post = main_cursor.fetchone()
        
        if not existing_post:
            try:
                main_cursor.execute("""
                    INSERT OR IGNORE INTO posts
                    (id, title, content, image_url, video_url, timestamp, updated_at, author_id, likes_count, comments_count)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (post_id, title, content, image_url, video_url, timestamp, updated_at, author_id, likes_count, comments_count))
            except sqlite3.IntegrityError as e:
                print(f"  帖子插入失败: {e}")
    
    # 复制视频数据
    print("复制视频数据...")
    original_cursor.execute("SELECT * FROM videos;")
    original_videos = original_cursor.fetchall()
    
    for video in original_videos:
        video_id, title, description, video_url, thumbnail_url, duration, views, likes_count, comments_count, timestamp, updated_at, uploader_id = video
        
        # 检查视频是否已存在
        main_cursor.execute("SELECT id FROM videos WHERE title = ? AND uploader_id = ?", (title, uploader_id))
        existing_video = main_cursor.fetchone()
        
        if not existing_video:
            try:
                main_cursor.execute("""
                    INSERT OR IGNORE INTO videos
                    (id, title, description, video_url, thumbnail_url, duration, views, likes_count, comments_count, timestamp, updated_at, uploader_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (video_id, title, description, video_url, thumbnail_url, duration, views, likes_count, comments_count, timestamp, updated_at, uploader_id))
            except sqlite3.IntegrityError as e:
                print(f"  视频插入失败: {e}")
    
    # 复制新闻数据
    print("复制新闻数据...")
    original_cursor.execute("SELECT * FROM news;")
    original_news = original_cursor.fetchall()
    
    for news in original_news:
        news_id, title, content, summary, image_url, source, timestamp, views, likes_count = news
        
        # 检查新闻是否已存在
        main_cursor.execute("SELECT id FROM news WHERE title = ?", (title,))
        existing_news = main_cursor.fetchone()
        
        if not existing_news:
            try:
                main_cursor.execute("""
                    INSERT OR IGNORE INTO news
                    (id, title, content, summary, image_url, source, timestamp, views, likes_count)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (news_id, title, content, summary, image_url, source, timestamp, views, likes_count))
            except sqlite3.IntegrityError as e:
                print(f"  新闻插入失败: {e}")
    
    # 提交更改
    main_conn.commit()
    
    # 验证合并结果
    main_cursor.execute("SELECT COUNT(*) FROM users;")
    final_users = main_cursor.fetchone()[0]
    main_cursor.execute("SELECT COUNT(*) FROM messages;")
    final_messages = main_cursor.fetchone()[0]
    main_cursor.execute("SELECT COUNT(*) FROM follows;")
    final_follows = main_cursor.fetchone()[0]
    
    print(f"\n合并完成!")
    print(f"最终用户数: {final_users}")
    print(f"最终消息数: {final_messages}")
    print(f"最终关注关系数: {final_follows}")
    
    # 特别显示您提到的重要用户
    important_users = ['FallPetal', '赵栋行001']
    for username in important_users:
        main_cursor.execute("SELECT id, username, email FROM users WHERE username LIKE ? OR email LIKE ?", (f'%{username}%', f'%{username}%'))
        user = main_cursor.fetchone()
        if user:
            print(f"重要用户 '{username}' 已找到: ID={user[0]}, Username={user[1]}, Email={user[2]}")
        else:
            print(f"重要用户 '{username}' 未找到")
    
    original_conn.close()
    main_conn.close()

if __name__ == "__main__":
    merge_databases()