'''
Author: your name
Date: 2026-01-11 22:49:58
LastEditTime: 2026-01-11 22:49:58
LastEditors: your name
Description: In User Settings Edit
FilePath: \Q文件\python_web_project\check_and_create_db.py
'''
from app import app, db
import sqlite3

def check_and_create_tables():
    # 创建数据库表
    with app.app_context():
        db.create_all()
        print('数据库表已创建')
    
    # 检查数据库表
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # 检查所有表
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print('数据库中的表:', tables)
    
    # 检查messages表是否存在
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='messages'")
    result = cursor.fetchone()
    if result:
        print('messages表存在')
        # 检查messages表中的数据
        cursor.execute('SELECT COUNT(*) FROM messages')
        count = cursor.fetchone()[0]
        print(f'messages表中有 {count} 条记录')
        
        # 如果有记录，查看最近的一些记录
        if count > 0:
            cursor.execute('SELECT id, attachment_path, attachment_filename FROM messages WHERE attachment_path IS NOT NULL LIMIT 5')
            records = cursor.fetchall()
            print('附件消息示例:')
            for record in records:
                print(f'  ID: {record[0]}, Path: {record[1]}, Filename: {record[2]}')
    else:
        print('messages表不存在')
    
    conn.close()

if __name__ == "__main__":
    check_and_create_tables()