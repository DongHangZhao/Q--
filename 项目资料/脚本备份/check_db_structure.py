'''
Author: your name
Date: 2026-01-11 22:49:28
LastEditTime: 2026-01-11 22:49:29
LastEditors: your name
Description: In User Settings Edit
FilePath: \Q文件\python_web_project\check_db_structure.py
'''
import sqlite3

def check_database_structure():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # 检查所有表
    cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
    tables = cursor.fetchall()
    print("数据库中的表:", tables)
    
    # 检查每个表的结构
    for table_name in tables:
        table_name = table_name[0]
        print(f"\n表 {table_name} 的结构:")
        cursor.execute(f'PRAGMA table_info({table_name})')
        columns = cursor.fetchall()
        for col in columns:
            print(f"  {col}")
    
    conn.close()

if __name__ == "__main__":
    check_database_structure()