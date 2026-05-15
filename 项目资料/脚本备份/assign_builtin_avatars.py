"""
为内置用户分配特定的头像图片
"""
from app import app, db
from models import User
import os


def assign_builtin_avatars():
    """为内置用户分配特定的头像图片"""
    with app.app_context():
        # 定义内置用户的特定头像映射
        builtin_users_avatars = {
            'admin': 'uploads/avatars/avatar_1.png',
            'tianmi': 'uploads/avatars/avatar_2.png',
            'FallPetal': 'uploads/avatars/avatar_3.png',
            'zhangsan': 'uploads/avatars/avatar_4.png',
            'lisi': 'uploads/avatars/avatar_5.png',
            'xiaoming': 'uploads/avatars/avatar_6.png',  # 新增
            'zhaoliu': 'uploads/avatars/avatar_7.png',   # 新增
            'wangwu': 'uploads/avatars/avatar_8.png',    # 新增
            'meimei': 'uploads/avatars/avatar_9.png'     # 新增
        }
        
        # 为每个内置用户分配头像
        for username, avatar_path in builtin_users_avatars.items():
            user = User.query.filter_by(username=username).first()
            if user:
                # 检查头像文件是否存在
                avatar_full_path = os.path.join('static', avatar_path)
                if os.path.exists(avatar_full_path):
                    # 检查当前头像是否已经是网络头像或旧的默认头像
                    if (user.avatar.startswith('http') or 
                        user.avatar.startswith('avatars/default_avatar') or
                        user.avatar == 'default_avatar.png'):
                        user.avatar = avatar_path
                        print(f"为用户 {username} 分配头像: {avatar_path}")
                    else:
                        print(f"用户 {username} 已有头像，跳过分配: {user.avatar}")
                else:
                    print(f"头像文件不存在: {avatar_full_path}")
            else:
                print(f"用户不存在: {username}")
        
        # 提交更改
        db.session.commit()
        print("内置用户头像分配完成")


if __name__ == '__main__':
    assign_builtin_avatars()