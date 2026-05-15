'''
Author: your name
Date: 2026-01-19 04:23:11
LastEditTime: 2026-01-19 04:23:11
LastEditors: your name
Description: In User Settings Edit
FilePath: \Q文件\python_web_project\check_original_db.py
'''
import sqlite3

# 连接到原始数据库
conn = sqlite3.connect('database/users.db')
cursor = conn.cursor()

print('=== 原始数据库 (database/users.db) 状态检查 ===')
print('数据库文件: database/users.db')
print()

# 检查所有表
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print('所有表:', [table[0] for table in tables])
print()

# 检查用户表
print('=== 用户信息 ===')
try:
    cursor.execute('SELECT id, username, email, join_date FROM users ORDER BY id;')
    users = cursor.fetchall()
    print(f'用户总数: {len(users)}')
    for user in users:
        print(f'  ID: {user[0]}, Username: {user[1]}, Email: {user[2]}, 注册时间: {user[3]}')
except sqlite3.OperationalError as e:
    print(f'用户表错误: {e}')
print()

# 检查关注关系
print('=== 关注关系 ===')
try:
    cursor.execute('SELECT COUNT(*) FROM follows;')
    follows_count = cursor.fetchone()[0]
    print(f'关注关系数量: {follows_count}')
    if follows_count > 0:
        cursor.execute('SELECT follower_id, followed_id FROM follows;')
        follows = cursor.fetchall()
        for follow in follows[:10]:  # 显示前10个
            print(f'  用户{follow[0]} -> 用户{follow[1]}')
except sqlite3.OperationalError as e:
    print(f'关注关系表错误: {e}')
print()

# 检查消息
print('=== 消息信息 ===')
try:
    cursor.execute('SELECT COUNT(*) FROM messages;')
    messages_count = cursor.fetchone()[0]
    print(f'消息数量: {messages_count}')
    if messages_count > 0:
        cursor.execute('SELECT id, sender_id, recipient_id, content FROM messages;')
        messages = cursor.fetchall()
        for msg in messages[:10]:  # 显示前10个
            print(f'  ID: {msg[0]}, 发送者: {msg[1]}, 接收者: {msg[2]}, 内容: {msg[3][:50]}...')
except sqlite3.OperationalError as e:
    print(f'消息表错误: {e}')
print()

conn.close()