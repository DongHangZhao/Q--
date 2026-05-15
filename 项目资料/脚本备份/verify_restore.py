'''
Author: your name
Date: 2026-01-19 04:37:18
LastEditTime: 2026-01-19 04:37:18
LastEditors: your name
Description: In User Settings Edit
FilePath: \Q文件\python_web_project\verify_restore.py
'''
import sqlite3

# 检查恢复的数据库
conn = sqlite3.connect('app.db')
cursor = conn.cursor()

print('=== 恢复后的数据库状态 ===')

# 检查用户表
cursor.execute('SELECT COUNT(*) FROM users;')
user_count = cursor.fetchone()[0]
print(f'用户数量: {user_count}')

# 检查消息表
cursor.execute('SELECT COUNT(*) FROM messages;')
msg_count = cursor.fetchone()[0]
print(f'消息数量: {msg_count}')

# 检查特定用户
cursor.execute("SELECT id, username, email FROM users WHERE username IN ('FallPetal', '赵栋行001');")
important_users = cursor.fetchall()
print('重要用户:')
for user in important_users:
    print(f'  ID: {user[0]}, Username: {user[1]}, Email: {user[2]}')

conn.close()
print('\n数据库已恢复到原始状态')