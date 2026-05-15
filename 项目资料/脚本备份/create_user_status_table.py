'''
Author: your name
Date: 2026-01-12 00:08:54
LastEditTime: 2026-01-12 00:08:55
LastEditors: your name
Description: In User Settings Edit
FilePath: \Q文件\python_web_project\create_user_status_table.py
'''
from app import app, db
from models import User, UserStatus
from datetime import datetime


def create_user_status_table():
    """创建用户状态表并初始化现有用户的状态"""
    with app.app_context():
        # 创建表
        db.create_all()
        print("用户状态表已创建")
        
        # 为现有用户初始化状态
        users = User.query.all()
        for user in users:
            existing_status = UserStatus.query.filter_by(user_id=user.id).first()
            if not existing_status:
                # 为现有用户创建初始状态，默认为离线
                status = UserStatus(
                    user_id=user.id,
                    is_online=False,
                    last_offline_time=user.last_seen or user.join_date
                )
                db.session.add(status)
                print(f"为用户 {user.username} 创建初始状态")
        
        db.session.commit()
        print("用户状态初始化完成")


if __name__ == "__main__":
    create_user_status_table()