'''
Author: your name
Date: 2026-01-12 00:16:26
LastEditTime: 2026-01-17 16:10:18
LastEditors: ZDH
Description: In User Settings Edit
FilePath: \Q文件\python_web_project\test_friend_features.py
'''
from app import app, db
from models import User, UserStatus
from datetime import datetime


def test_friend_features():
    """测试好友功能是否正常"""
    with app.app_context():
        print("=== 测试好友功能 ===")
        
        # 检查用户状态表是否已创建
        try:
            user_statuses = UserStatus.query.all()
            print(f"✓ 用户状态表已创建，共有 {len(user_statuses)} 条记录")
        except Exception as e:
            print(f"✗ 用户状态表存在问题: {e}")
            return
        
        # 检查是否有用户状态记录
        if user_statuses:
            for status in user_statuses[:3]:  # 只显示前3个
                user = User.query.get(status.user_id)
                print(f"- 用户 {user.username if user else 'Unknown'}: "
                      f"{'在线' if status.is_online else '离线'}, "
                      f"最后上线时间: {status.last_online_time}, "
                      f"最后下线时间: {status.last_offline_time}")
        
        # 检查用户是否有关注关系
        users = User.query.limit(5).all()
        for user in users:
            following_count = user.get_following_count()
            followers_count = user.get_followers_count()
            print(f"- 用户 {user.username}: 关注 {following_count} 人, 粉丝 {followers_count} 人")
        
        print("=== 测试完成 ===")


if __name__ == "__main__":
    test_friend_features()