'''
Author: your name
Date: 2026-01-11 18:43:09
LastEditTime: 2026-01-11 18:43:10
LastEditors: your name
Description: In User Settings Edit
FilePath: \Q文件\python_web_project\verify_db_structure.py
'''
import sqlite3
import os

# 数据库文件路径
db_path = os.path.join('database', 'users.db')

# 连接到数据库
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # 检查messages表的所有列
    cursor.execute("PRAGMA table_info(messages)")
    columns = cursor.fetchall()
    
    print("Messages表的当前列结构:")
    print("序号 | 名称 | 类型 | 非空 | 默认值 | 主键")
    print("-" * 50)
    for i, col in enumerate(columns):
        print(f"{i+1} | {col[1]} | {col[2]} | {col[3]} | {col[4]} | {col[5]}")
    
    # 检查必要的附件字段是否存在
    column_names = [col[1] for col in columns]
    required_columns = ['attachment_path', 'attachment_type', 'attachment_filename']
    
    print("\n检查必需的附件字段:")
    all_present = True
    for req_col in required_columns:
        if req_col in column_names:
            print(f"✓ {req_col} - 存在")
        else:
            print(f"✗ {req_col} - 缺失")
            all_present = False
    
    if all_present:
        print("\n✓ 所有必需的附件字段均已存在，数据库结构已正确更新！")
    else:
        print("\n✗ 数据库结构更新不完整！")

except sqlite3.Error as e:
    print(f"数据库操作错误: {e}")
    
finally:
    conn.close()