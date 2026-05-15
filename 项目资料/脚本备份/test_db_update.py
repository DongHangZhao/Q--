'''
Author: your name
Date: 2026-01-11 18:56:24
LastEditTime: 2026-01-11 18:56:24
LastEditors: your name
Description: In User Settings Edit
FilePath: \Q文件\python_web_project\test_db_update.py
'''
import sqlite3
import os

# 数据库文件路径
db_path = os.path.join('database', 'users.db')

# 连接到数据库
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # 检查messages表的详细信息
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='messages'")
    table_info = cursor.fetchone()
    
    if table_info:
        print("Messages表的CREATE语句:")
        print(table_info[0])
    else:
        print("未找到messages表")
    
    # 检查messages表的所有列
    cursor.execute("PRAGMA table_info(messages)")
    columns = cursor.fetchall()
    
    print("\nMessages表的当前列结构:")
    print("序号 | 名称 | 类型 | 非空 | 默认值 | 主键")
    print("-" * 50)
    for i, col in enumerate(columns):
        print(f"{i+1} | {col[1]} | {col[2]} | {col[3]} | {col[4]} | {col[5]}")
    
    # 测试插入一条带附件的消息
    print("\n正在测试插入一条带附件的消息...")
    cursor.execute("""
        INSERT INTO messages (sender_id, recipient_id, content, timestamp, attachment_path, attachment_type, attachment_filename) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (1, 2, '测试消息', '2026-01-11 12:00:00', 'static/uploads/attachments/test.jpg', 'image', 'test.jpg'))
    
    # 获取刚插入的记录
    cursor.execute("SELECT * FROM messages WHERE content='测试消息'")
    test_record = cursor.fetchone()
    
    print(f"插入的测试记录: {test_record}")
    
    # 回滚测试插入
    conn.rollback()
    print("测试回滚完成")

except sqlite3.Error as e:
    print(f"数据库操作错误: {e}")
    
finally:
    conn.close()

print("\n数据库验证完成！")