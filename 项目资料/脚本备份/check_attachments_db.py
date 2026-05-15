'''
Author: your name
Date: 2026-01-11 22:50:38
LastEditTime: 2026-01-11 22:50:38
LastEditors: your name
Description: In User Settings Edit
FilePath: \Q文件\python_web_project\check_attachments_db.py
'''
from app import app, db

def check_messages_with_attachments():
    with app.app_context():
        # 查询所有带附件的消息
        result = db.session.execute(
            db.text('SELECT id, attachment_path, attachment_filename, attachment_type FROM messages WHERE attachment_path IS NOT NULL')
        )
        rows = result.fetchall()
        
        print("所有带附件的消息:")
        for row in rows:
            print(f"ID: {row[0]}, Path: {row[1]}, Filename: {row[2]}, Type: {row[3]}")
        
        # 特别查询视频附件
        result = db.session.execute(
            db.text("SELECT id, attachment_path, attachment_filename FROM messages WHERE attachment_type = 'video'")
        )
        video_rows = result.fetchall()
        
        print("\n视频附件:")
        for row in video_rows:
            print(f"ID: {row[0]}, Path: {row[1]}, Filename: {row[2]}")

if __name__ == "__main__":
    check_messages_with_attachments()