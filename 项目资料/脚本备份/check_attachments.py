'''
Author: your name
Date: 2026-01-11 22:49:15
LastEditTime: 2026-01-11 22:49:15
LastEditors: your name
Description: In User Settings Edit
FilePath: \Q文件\python_web_project\check_attachments.py
'''
import sqlite3

def check_attachments():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # 查询所有带附件的消息
    cursor.execute('SELECT id, attachment_path, attachment_filename FROM messages WHERE attachment_path IS NOT NULL')
    rows = cursor.fetchall()
    
    print("所有带附件的消息:")
    for row in rows:
        print(f"ID: {row[0]}, Path: {row[1]}, Filename: {row[2]}")
    
    # 特别查询视频附件
    cursor.execute('SELECT id, attachment_path, attachment_filename FROM messages WHERE attachment_path LIKE ?', ('%.mp4%',))
    video_rows = cursor.fetchall()
    
    print("\n视频附件:")
    for row in video_rows:
        print(f"ID: {row[0]}, Path: {row[1]}, Filename: {row[2]}")
    
    conn.close()

if __name__ == "__main__":
    check_attachments()