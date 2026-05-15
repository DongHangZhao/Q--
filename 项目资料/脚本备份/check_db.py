'''
Author: your name
Date: 2026-01-19 03:49:06
LastEditTime: 2026-01-19 03:49:06
LastEditors: your name
Description: In User Settings Edit
FilePath: \Q文件\python_web_project\check_db.py
'''
from app import app, db
import os
import sqlite3

print('检查数据库文件...')
if os.path.exists('app.db'):
    print('app.db存在')
else:
    print('app.db不存在，创建应用上下文并创建数据库...')
    with app.app_context():
        db.create_all()
    print('数据库已创建')

conn = sqlite3.connect('app.db')
cursor = conn.cursor()
cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
tables = cursor.fetchall()
print('数据库表:', tables)

cursor.execute('PRAGMA table_info(comments)')
rows = cursor.fetchall()
print('Comments表结构:')
for row in rows:
    print(row)

conn.close()