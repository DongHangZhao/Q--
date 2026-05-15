'''
Author: your name
Date: 2026-01-11 22:50:25
LastEditTime: 2026-01-11 22:50:25
LastEditors: your name
Description: In User Settings Edit
FilePath: \Q文件\python_web_project\check_messages_table.py
'''
from app import app, db

def check_messages_table():
    with app.app_context():
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        columns = inspector.get_columns('messages')
        print('messages表的列结构:')
        for col in columns:
            print(f'  {col["name"]}: {col["type"]}')

if __name__ == "__main__":
    check_messages_table()