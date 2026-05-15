"""
咫尺天涯社交平台 - 更新内置用户头像
"""

from app import app, db
from models import User


def update_builtin_user_avatars():
    """更新内置用户的头像"""
    with app.app_context():
        # 定义内置用户的特定头像
        builtin_avatars = {
            'admin': 'default_avatar_admin.png',
            'tianmi': 'default_avatar_tianmi.png', 
            'FallPetal': 'default_avatar_fallpetal.png',
            'zhangsan': 'default_avatar_zhangsan.png',
            'lisi': 'default_avatar_lisi.png'
        }

        for username, avatar in builtin_avatars.items():
            user = User.query.filter_by(username=username).first()
            if user:
                # 如果用户当前使用的是随机网络头像或默认头像，则更新为特定头像
                if user.avatar.startswith('http') or user.avatar == 'default_avatar.png':
                    user.avatar = avatar
                    print(f"更新用户 {username} 的头像为 {avatar}")
        
        db.session.commit()
        print("内置用户头像更新完成")


if __name__ == '__main__':
    update_builtin_user_avatars()