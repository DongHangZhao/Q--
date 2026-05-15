'''
Author: your name
Date: 2026-01-19 04:29:03
LastEditTime: 2026-01-19 04:29:03
LastEditors: your name
Description: In User Settings Edit
FilePath: \Q文件\python_web_project\fix_timestamps.py
'''
import sqlite3
from datetime import datetime
import re

def fix_timestamps():
    # 连接数据库
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    
    print("开始修复数据库时间戳...")
    
    # 修复posts表的时间戳
    print("修复posts表时间戳...")
    try:
        cursor.execute("SELECT id, timestamp FROM posts WHERE timestamp IS NOT NULL")
        posts = cursor.fetchall()
        for post in posts:
            post_id, timestamp = post
            # 检查时间戳格式是否正确
            if timestamp and isinstance(timestamp, str):
                # 尝试解析时间戳
                try:
                    # 如果已经是正确格式，跳过
                    parsed = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                except ValueError:
                    # 如果格式不正确，设置为当前时间
                    print(f"修复post {post_id} 的时间戳: {timestamp}")
                    cursor.execute("UPDATE posts SET timestamp = ? WHERE id = ?", 
                                 (datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f'), post_id))
    except Exception as e:
        print(f"处理posts表时出错: {e}")
    
    # 修复posts表的updated_at字段
    print("修复posts表updated_at字段...")
    try:
        cursor.execute("SELECT id, updated_at FROM posts WHERE updated_at IS NOT NULL")
        posts = cursor.fetchall()
        for post in posts:
            post_id, timestamp = post
            if timestamp and isinstance(timestamp, str):
                try:
                    parsed = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                except ValueError:
                    print(f"修复post {post_id} 的updated_at: {timestamp}")
                    cursor.execute("UPDATE posts SET updated_at = ? WHERE id = ?", 
                                 (datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f'), post_id))
    except Exception as e:
        print(f"处理posts updated_at时出错: {e}")
    
    # 修复videos表的时间戳
    print("修复videos表时间戳...")
    try:
        cursor.execute("SELECT id, timestamp FROM videos WHERE timestamp IS NOT NULL")
        videos = cursor.fetchall()
        for video in videos:
            video_id, timestamp = video
            if timestamp and isinstance(timestamp, str):
                try:
                    parsed = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                except ValueError:
                    print(f"修复video {video_id} 的时间戳: {timestamp}")
                    cursor.execute("UPDATE videos SET timestamp = ? WHERE id = ?", 
                                 (datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f'), video_id))
    
        # 修复videos表的updated_at字段
        cursor.execute("SELECT id, updated_at FROM videos WHERE updated_at IS NOT NULL")
        videos = cursor.fetchall()
        for video in videos:
            video_id, timestamp = video
            if timestamp and isinstance(timestamp, str):
                try:
                    parsed = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                except ValueError:
                    print(f"修复video {video_id} 的updated_at: {timestamp}")
                    cursor.execute("UPDATE videos SET updated_at = ? WHERE id = ?", 
                                 (datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f'), video_id))
    except Exception as e:
        print(f"处理videos表时出错: {e}")
    
    # 修复messages表的时间戳
    print("修复messages表时间戳...")
    try:
        cursor.execute("SELECT id, timestamp FROM messages WHERE timestamp IS NOT NULL")
        messages = cursor.fetchall()
        for msg in messages:
            msg_id, timestamp = msg
            if timestamp and isinstance(timestamp, str):
                try:
                    parsed = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                except ValueError:
                    print(f"修复message {msg_id} 的时间戳: {timestamp}")
                    cursor.execute("UPDATE messages SET timestamp = ? WHERE id = ?", 
                                 (datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f'), msg_id))
    except Exception as e:
        print(f"处理messages表时出错: {e}")
    
    # 修复news表的时间戳
    print("修复news表时间戳...")
    try:
        cursor.execute("SELECT id, timestamp FROM news WHERE timestamp IS NOT NULL")
        news_items = cursor.fetchall()
        for news in news_items:
            news_id, timestamp = news
            if timestamp and isinstance(timestamp, str):
                try:
                    parsed = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                except ValueError:
                    print(f"修复news {news_id} 的时间戳: {timestamp}")
                    cursor.execute("UPDATE news SET timestamp = ? WHERE id = ?", 
                                 (datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f'), news_id))
    except Exception as e:
        print(f"处理news表时出错: {e}")
    
    # 修复comments表的时间戳
    print("修复comments表时间戳...")
    try:
        cursor.execute("SELECT id, timestamp FROM comments WHERE timestamp IS NOT NULL")
        comments = cursor.fetchall()
        for comment in comments:
            comment_id, timestamp = comment
            if timestamp and isinstance(timestamp, str):
                try:
                    parsed = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                except ValueError:
                    print(f"修复comment {comment_id} 的时间戳: {timestamp}")
                    cursor.execute("UPDATE comments SET timestamp = ? WHERE id = ?", 
                                 (datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f'), comment_id))
    except Exception as e:
        print(f"处理comments表时出错: {e}")
    
    # 修复user_status表的时间戳
    print("修复user_status表时间戳...")
    try:
        for col in ['last_online_time', 'last_offline_time', 'created_at', 'updated_at']:
            cursor.execute(f"SELECT id, {col} FROM user_status WHERE {col} IS NOT NULL")
            statuses = cursor.fetchall()
            for status in statuses:
                status_id, timestamp = status
                if timestamp and isinstance(timestamp, str):
                    try:
                        parsed = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    except ValueError:
                        print(f"修复user_status {status_id} 的{col}: {timestamp}")
                        cursor.execute(f"UPDATE user_status SET {col} = ? WHERE id = ?", 
                                     (datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f'), status_id))
    except Exception as e:
        print(f"处理user_status表时出错: {e}")
    
    # 修复follows表的时间戳
    print("修复follows表时间戳...")
    try:
        cursor.execute("SELECT id, timestamp FROM follows WHERE timestamp IS NOT NULL")
        follows = cursor.fetchall()
        for follow in follows:
            follow_id, timestamp = follow
            if timestamp and isinstance(timestamp, str):
                try:
                    parsed = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                except ValueError:
                    print(f"修复follow {follow_id} 的时间戳: {timestamp}")
                    cursor.execute("UPDATE follows SET timestamp = ? WHERE id = ?", 
                                 (datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f'), follow_id))
    except Exception as e:
        print(f"处理follows表时出错: {e}")
    
    # 修复content_history表的时间戳
    print("修复content_history表时间戳...")
    try:
        cursor.execute("SELECT id, timestamp FROM content_history WHERE timestamp IS NOT NULL")
        histories = cursor.fetchall()
        for hist in histories:
            hist_id, timestamp = hist
            if timestamp and isinstance(timestamp, str):
                try:
                    parsed = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                except ValueError:
                    print(f"修复content_history {hist_id} 的时间戳: {timestamp}")
                    cursor.execute("UPDATE content_history SET timestamp = ? WHERE id = ?", 
                                 (datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f'), hist_id))
    except Exception as e:
        print(f"处理content_history表时出错: {e}")
    
    # 修复news_likes表的时间戳
    print("修复news_likes表时间戳...")
    try:
        cursor.execute("SELECT id, timestamp FROM news_likes WHERE timestamp IS NOT NULL")
        likes = cursor.fetchall()
        for like in likes:
            like_id, timestamp = like
            if timestamp and isinstance(timestamp, str):
                try:
                    parsed = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                except ValueError:
                    print(f"修复news_like {like_id} 的时间戳: {timestamp}")
                    cursor.execute("UPDATE news_likes SET timestamp = ? WHERE id = ?", 
                                 (datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f'), like_id))
    except Exception as e:
        print(f"处理news_likes表时出错: {e}")
    
    # 修复post_likes表的时间戳
    print("修复post_likes表时间戳...")
    try:
        cursor.execute("SELECT id, timestamp FROM post_likes WHERE timestamp IS NOT NULL")
        likes = cursor.fetchall()
        for like in likes:
            like_id, timestamp = like
            if timestamp and isinstance(timestamp, str):
                try:
                    parsed = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                except ValueError:
                    print(f"修复post_like {like_id} 的时间戳: {timestamp}")
                    cursor.execute("UPDATE post_likes SET timestamp = ? WHERE id = ?", 
                                 (datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f'), like_id))
    except Exception as e:
        print(f"处理post_likes表时出错: {e}")
    
    # 修复video_likes表的时间戳
    print("修复video_likes表时间戳...")
    try:
        cursor.execute("SELECT id, timestamp FROM video_likes WHERE timestamp IS NOT NULL")
        likes = cursor.fetchall()
        for like in likes:
            like_id, timestamp = like
            if timestamp and isinstance(timestamp, str):
                try:
                    parsed = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                except ValueError:
                    print(f"修复video_like {like_id} 的时间戳: {timestamp}")
                    cursor.execute("UPDATE video_likes SET timestamp = ? WHERE id = ?", 
                                 (datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f'), like_id))
    except Exception as e:
        print(f"处理video_likes表时出错: {e}")
    
    # 提交更改
    conn.commit()
    print("时间戳修复完成！")
    
    # 验证修复结果
    print("\n验证修复结果...")
    tables_to_check = ['posts', 'messages', 'videos', 'news', 'comments']
    for table in tables_to_check:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{table} 表记录数: {count}")
        if count > 0:
            cursor.execute(f"SELECT timestamp FROM {table} LIMIT 1")
            sample = cursor.fetchone()
            if sample:
                print(f"  示例时间戳: {sample[0]} (类型: {type(sample[0])})")
    
    conn.close()

if __name__ == "__main__":
    fix_timestamps()