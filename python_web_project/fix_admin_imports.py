'''
Author: your name
Date: 2026-04-29 16:26:50
LastEditTime: 2026-04-29 16:26:51
LastEditors: your name
Description: In User Settings Edit
FilePath: \Q文件\python_web_project\fix_admin_imports.py
'''
# -*- coding: utf-8 -*-
import sys

# 读取文件
with open('admin_panel.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到需要插入的位置
insert_after_line = None
for i, line in enumerate(lines):
    if 'from flask_login import current_user' in line:
        insert_after_line = i
        break

if insert_after_line is None:
    print("错误：找不到插入点")
    sys.exit(1)

# 检查是否已经导入
already_imported = any('from models import' in line for line in lines)

if already_imported:
    print("models导入已存在")
else:
    # 插入导入语句
    import_lines = [
        '\n',
        '# ===================== 一次性导入所有模型（修复所有未定义错误）=====================\n',
        'from models import (\n',
        '    User, Follows, UserStatus,\n',
        '    Post, News, Video,\n',
        '    Comment, Message, Trending, ContentHistory,\n',
        '    NewsLike, PostLike, VideoLike,\n',
        '    NewsOperationLog, PasswordResetRequest, PasswordChangeLog\n',
        ')\n',
    ]

    # 在insert_after_line之后插入
    for j, import_line in enumerate(import_lines):
        lines.insert(insert_after_line + 1 + j, import_line)

    # 写回文件
    with open('admin_panel.py', 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print("✅ 已成功添加models导入语句")

# 验证
with open('admin_panel.py', 'r', encoding='utf-8') as f:
    content = f.read()
    if 'from models import' in content and 'User' in content:
        print("✅ 验证成功：导入语句已正确添加")
    else:
        print("❌ 验证失败")
