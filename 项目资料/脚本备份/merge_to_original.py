'''
Author: your name
Date: 2026-01-19 04:41:21
LastEditTime: 2026-01-19 04:41:21
LastEditors: your name
Description: In User Settings Edit
FilePath: \Q文件\python_web_project\merge_to_original.py
'''
import sqlite3
from datetime import datetime

def merge_to_original_db():
    # 连接两个数据库
    current_db = sqlite3.connect('app.db')
    original_db = sqlite3.connect('database/users.db')
    
    current_cursor = current_db.cursor()
    original_cursor = original_db.cursor()
    
    print("开始将当前数据库的数据合并到原始数据库...")
    
    # 首先检查原始数据库中已有的用户
    original_cursor.execute("SELECT id, username, email FROM users ORDER BY id DESC LIMIT 1;")
    result = original_cursor.fetchone()
    max_user_id_in_original = result[0] if result else 0
    print(f"原始数据库中最大用户ID: {max_user_id_in_original}")
    
    # 从当前数据库获取用户数据
    current_cursor.execute("SELECT id, username, email, password_hash, avatar, bio, location, website, is_active, is_banned, can_post, can_video, can_comment, is_admin, join_date, last_seen FROM users ORDER BY id;")
    current_users = current_cursor.fetchall()
    
    # 合并用户数据
    users_mapping = {}  # 用于映射ID变化
    for user in current_users:
        user_id, username, email, password_hash, avatar, bio, location, website, is_active, is_banned, can_post, can_video, can_comment, is_admin, join_date, last_seen = user
        
        # 检查用户是否已存在于原始数据库中
        original_cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?", (username, email))
        existing_user = original_cursor.fetchone()
        
        if existing_user:
            # 如果用户已存在，记录ID映射
            users_mapping[user_id] = existing_user[0]
            print(f"用户 {username} 已存在，ID: {existing_user[0]}")
        else:
            # 如果用户不存在，插入新用户并记录ID映射
            new_user_id = max_user_id_in_original + 1
            users_mapping[user_id] = new_user_id
            
            try:
                original_cursor.execute("""
                    INSERT INTO users 
                    (id, username, email, password_hash, avatar, bio, location, website, 
                     is_active, is_banned, can_post, can_video, can_comment, is_admin, join_date, last_seen)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (new_user_id, username, email, password_hash, avatar, bio, location, website, 
                      is_active, is_banned, can_post, can_video, can_comment, is_admin, join_date, last_seen))
                
                max_user_id_in_original = new_user_id
                print(f"添加新用户 {username}, 新ID: {new_user_id}")
            except sqlite3.IntegrityError as e:
                print(f"插入用户 {username} 时出错: {e}")
    
    # 合并帖子数据
    print("合并帖子数据...")
    current_cursor.execute("SELECT id, title, content, image_url, video_url, timestamp, updated_at, author_id, likes_count, comments_count FROM posts;")
    posts = current_cursor.fetchall()
    
    for post in posts:
        post_id, title, content, image_url, video_url, timestamp, updated_at, author_id, likes_count, comments_count = post
        
        # 映射作者ID
        new_author_id = users_mapping.get(author_id, author_id)
        
        # 检查帖子是否已存在
        original_cursor.execute("SELECT id FROM posts WHERE title = ? AND author_id = ?", (title, new_author_id))
        existing_post = original_cursor.fetchone()
        
        if not existing_post:
            try:
                original_cursor.execute("""
                    INSERT OR IGNORE INTO posts
                    (id, title, content, image_url, video_url, timestamp, updated_at, author_id, likes_count, comments_count)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (post_id, title, content, image_url, video_url, timestamp, updated_at, new_author_id, likes_count, comments_count))
            except sqlite3.IntegrityError as e:
                print(f"插入帖子 {title} 时出错: {e}")
    
    # 合并视频数据
    print("合并视频数据...")
    current_cursor.execute("SELECT id, title, description, video_url, thumbnail_url, duration, views, likes_count, comments_count, timestamp, updated_at, uploader_id FROM videos;")
    videos = current_cursor.fetchall()
    
    for video in videos:
        vid, title, description, video_url, thumbnail_url, duration, views, likes_count, comments_count, timestamp, updated_at, uploader_id = video
        
        # 映射上传者ID
        new_uploader_id = users_mapping.get(uploader_id, uploader_id)
        
        # 检查视频是否已存在
        original_cursor.execute("SELECT id FROM videos WHERE title = ? AND uploader_id = ?", (title, new_uploader_id))
        existing_video = original_cursor.fetchone()
        
        if not existing_video:
            try:
                original_cursor.execute("""
                    INSERT OR IGNORE INTO videos
                    (id, title, description, video_url, thumbnail_url, duration, views, likes_count, comments_count, timestamp, updated_at, uploader_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (vid, title, description, video_url, thumbnail_url, duration, views, likes_count, comments_count, timestamp, updated_at, new_uploader_id))
            except sqlite3.IntegrityError as e:
                print(f"插入视频 {title} 时出错: {e}")
    
    # 合并消息数据
    print("合并消息数据...")
    current_cursor.execute("SELECT id, sender_id, recipient_id, content, timestamp, is_read, message_type, related_id, related_type, attachment_path, attachment_type, attachment_filename FROM messages;")
    messages = current_cursor.fetchall()
    
    for msg in messages:
        msg_id, sender_id, recipient_id, content, timestamp, is_read, message_type, related_id, related_type, attachment_path, attachment_type, attachment_filename = msg
        
        # 映射发送者和接收者ID
        new_sender_id = users_mapping.get(sender_id, sender_id)
        new_recipient_id = users_mapping.get(recipient_id, recipient_id)
        
        # 检查消息是否已存在
        original_cursor.execute("SELECT id FROM messages WHERE content = ? AND sender_id = ? AND recipient_id = ? AND timestamp = ?", 
                               (content, new_sender_id, new_recipient_id, timestamp))
        existing_msg = original_cursor.fetchone()
        
        if not existing_msg:
            try:
                original_cursor.execute("""
                    INSERT OR IGNORE INTO messages
                    (id, sender_id, recipient_id, content, timestamp, is_read, message_type, 
                     related_id, related_type, attachment_path, attachment_type, attachment_filename)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (msg_id, new_sender_id, new_recipient_id, content, timestamp, is_read, message_type, 
                      related_id, related_type, attachment_path, attachment_type, attachment_filename))
            except sqlite3.IntegrityError as e:
                print(f"插入消息 '{content[:20]}...' 时出错: {e}")
    
    # 合并关注关系
    print("合并关注关系...")
    current_cursor.execute("SELECT follower_id, followed_id, timestamp FROM follows;")
    follows = current_cursor.fetchall()
    
    for follow in follows:
        follower_id, followed_id, timestamp = follow
        
        # 映射关注者和被关注者ID
        new_follower_id = users_mapping.get(follower_id, follower_id)
        new_followed_id = users_mapping.get(followed_id, followed_id)
        
        # 检查关注关系是否已存在
        original_cursor.execute("SELECT 1 FROM follows WHERE follower_id = ? AND followed_id = ?", (new_follower_id, new_followed_id))
        existing_follow = original_cursor.fetchone()
        
        if not existing_follow:
            try:
                original_cursor.execute("INSERT OR IGNORE INTO follows (follower_id, followed_id, timestamp) VALUES (?, ?, ?)", 
                                       (new_follower_id, new_followed_id, timestamp))
            except sqlite3.IntegrityError as e:
                print(f"插入关注关系 {new_follower_id} -> {new_followed_id} 时出错: {e}")
    
    # 合并新闻数据
    print("合并新闻数据...")
    current_cursor.execute("SELECT id, title, content, summary, image_url, source, timestamp, views, likes_count FROM news;")
    news_items = current_cursor.fetchall()
    
    for news in news_items:
        nid, title, content, summary, image_url, source, timestamp, views, likes_count = news
        
        # 检查新闻是否已存在
        original_cursor.execute("SELECT id FROM news WHERE title = ?", (title,))
        existing_news = original_cursor.fetchone()
        
        if not existing_news:
            try:
                original_cursor.execute("""
                    INSERT OR IGNORE INTO news
                    (id, title, content, summary, image_url, source, timestamp, views, likes_count)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (nid, title, content, summary, image_url, source, timestamp, views, likes_count))
            except sqlite3.IntegrityError as e:
                print(f"插入新闻 {title} 时出错: {e}")
    
    # 提交更改
    original_db.commit()
    
    # 统计合并结果
    original_cursor.execute("SELECT COUNT(*) FROM users;")
    final_users = original_cursor.fetchone()[0]
    original_cursor.execute("SELECT COUNT(*) FROM messages;")
    final_messages = original_cursor.fetchone()[0]
    original_cursor.execute("SELECT COUNT(*) FROM follows;")
    final_follows = original_cursor.fetchone()[0]
    original_cursor.execute("SELECT COUNT(*) FROM posts;")
    final_posts = original_cursor.fetchone()[0]
    original_cursor.execute("SELECT COUNT(*) FROM videos;")
    final_videos = original_cursor.fetchone()[0]
    
    print(f"\n合并完成!")
    print(f"原始数据库最终状态:")
    print(f"  用户数: {final_users}")
    print(f"  消息数: {final_messages}")
    print(f"  关注关系数: {final_follows}")
    print(f"  帖子数: {final_posts}")
    print(f"  视频数: {final_videos}")
    
    # 验证重要用户是否存在
    important_users = ['FallPetal', '赵栋行001']
    for username in important_users:
        original_cursor.execute("SELECT id, username, email FROM users WHERE username = ?", (username,))
        user = original_cursor.fetchone()
        if user:
            print(f"  重要用户 '{username}' 已找到: ID={user[0]}, Email={user[2]}")
        else:
            print(f"  重要用户 '{username}' 未找到")
    
    current_db.close()
    original_db.close()
    
    print(f"\n数据已成功合并到原始数据库 'database/users.db'")
    print(f"现在您可以使用原始数据库文件了")

if __name__ == "__main__":
    merge_to_original_db()