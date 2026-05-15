'''
Author: your name
Date: 2026-04-29 17:07:17
LastEditTime: 2026-04-29 17:07:17
LastEditors: your name
Description: In User Settings Edit
FilePath: \Q文件\python_web_project\fix_circular_import.py
'''
# -*- coding: utf-8 -*-
"""
修复admin_panel.py的循环导入问题
"""

# 读取文件
with open('admin_panel.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 替换错误的导入
old_import = 'from app import app, db'
new_import = ''

if old_import in content:
    content = content.replace(old_import, new_import)
    print("✅ 已移除 from app import app, db")
else:
    print("⚠️  未找到 'from app import app, db'")

# 修改models导入，添加db
old_models = '''from models import (
    User, Follows, UserStatus,
    Post, News, Video,
    Comment, Message, Trending, ContentHistory,
    NewsLike, PostLike, VideoLike,
    NewsOperationLog, PasswordResetRequest, PasswordChangeLog
)'''

new_models = '''from models import (
    db, User, Follows, UserStatus,
    Post, News, Video,
    Comment, Message, Trending, ContentHistory,
    NewsLike, PostLike, VideoLike,
    NewsOperationLog, PasswordResetRequest, PasswordChangeLog
)'''

if old_models in content and 'db, User' not in content:
    content = content.replace(old_models, new_models)
    print("✅ 已在models导入中添加db")
else:
    print("⚠️  models导入已包含db或格式不匹配")

# 写回文件
with open('admin_panel.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ 修复完成！")
print("\n验证导入语句：")
with open('admin_panel.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for i, line in enumerate(lines[18:22], start=19):
        print(f"{i}: {line.rstrip()}")
