import sqlite3
import os

# 数据库文件路径 - 使用与配置文件中相同的路径
db_path = os.path.join('database', 'users.db')

# 检查数据库文件是否存在
if not os.path.exists(db_path):
    print(f"数据库文件不存在: {db_path}")
    print("如果数据库是内存数据库或尚未创建，请先运行应用初始化")
    # 创建数据库文件（如果不存在）
    conn = sqlite3.connect(db_path)
    conn.close()
    print(f"已创建数据库文件: {db_path}")

print(f"正在更新数据库: {db_path}")

# 连接到数据库
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # 检查是否已存在attachment_path列
    cursor.execute("PRAGMA table_info(messages)")
    columns = [column[1] for column in cursor.fetchall()]
    
    # 添加缺失的列
    if 'attachment_path' not in columns:
        cursor.execute("ALTER TABLE messages ADD COLUMN attachment_path TEXT")
        print("已添加 attachment_path 列")
    else:
        print("attachment_path 列已存在")
    
    if 'attachment_type' not in columns:
        cursor.execute("ALTER TABLE messages ADD COLUMN attachment_type TEXT")
        print("已添加 attachment_type 列")
    else:
        print("attachment_type 列已存在")
    
    if 'attachment_filename' not in columns:
        cursor.execute("ALTER TABLE messages ADD COLUMN attachment_filename TEXT")
        print("已添加 attachment_filename 列")
    else:
        print("attachment_filename 列已存在")
    
    # 为了确保兼容性，也检查timestamp列是否存在（以防万一）
    if 'timestamp' not in columns:
        cursor.execute("ALTER TABLE messages ADD COLUMN timestamp DATETIME DEFAULT CURRENT_TIMESTAMP")
        print("已添加 timestamp 列")
    else:
        print("timestamp 列已存在")
    
    # 提交更改
    conn.commit()
    print("数据库更新成功！")
    
    # 验证更新
    cursor.execute("PRAGMA table_info(messages)")
    updated_columns = cursor.fetchall()
    print("\n更新后的Messages表结构:")
    for col in updated_columns:
        print(f"  {col[1]} ({col[2]}) - Not Null: {col[3]}, Default: {col[4]}, PK: {col[5]}")
    
except sqlite3.Error as e:
    print(f"数据库操作错误: {e}")
    conn.rollback()
    
finally:
    conn.close()
    print("数据库连接已关闭")