'''
Author: your name
Date: 2026-04-29 17:08:00
LastEditTime: 2026-04-29 17:08:01
LastEditors: your name
Description: In User Settings Edit
FilePath: \Q文件\python_web_project\fix_imports_once_and_for_all.py
'''
# -*- coding: utf-8 -*-
"""
彻底修复admin_panel.py导入问题
"""

# 读取文件
with open('admin_panel.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 找到插入位置
marker = '# ===================== 一次性导入所有模型（修复所有未定义错误）====================='

if marker in content and 'from models import' not in content:
    # 在marker后添加导入
    import_code = '''# ===================== 一次性导入所有模型（修复所有未定义错误）=====================
from models import (
    db, User, Follows, UserStatus,
    Post, News, Video,
    Comment, Message, Trending, ContentHistory,
    NewsLike, PostLike, VideoLike,
    NewsOperationLog, PasswordResetRequest, PasswordChangeLog
)

'''
    content = content.replace(marker, import_code)

    # 写回文件
    with open('admin_panel.py', 'w', encoding='utf-8') as f:
        f.write(content)

    print("✅ 已成功添加models导入（包含db）")
else:
    print("⚠️  导入可能已存在或标记找不到")

# 验证
with open('admin_panel.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    print("\n当前导入部分：")
    for i, line in enumerate(lines[18:35], start=19):
        print(f"{i}: {line.rstrip()}")
