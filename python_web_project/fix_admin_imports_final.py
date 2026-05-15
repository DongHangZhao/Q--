'''
Author: your name
Date: 2026-04-29 16:53:38
LastEditTime: 2026-04-29 16:53:38
LastEditors: your name
Description: In User Settings Edit
FilePath: \Q文件\python_web_project\fix_admin_imports_final.py
'''
# -*- coding: utf-8 -*-
"""
修复admin_panel.py的导入问题
"""

# 读取文件
with open('admin_panel.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 检查是否已经有models导入
if 'from models import' not in content:
    print("❌ 发现缺少models导入，正在修复...")

    # 找到插入位置
    insert_marker = '# ===================== 一次性导入所有模型（修复所有未定义错误）=====================\n\n# ===================== 一次性导入所有模型（修复所有未定义错误）====================='

    if insert_marker in content:
        # 替换为正确的导入
        correct_import = '''# ===================== 一次性导入所有模型（修复所有未定义错误）=====================
from models import (
    User, Follows, UserStatus,
    Post, News, Video,
    Comment, Message, Trending, ContentHistory,
    NewsLike, PostLike, VideoLike,
    NewsOperationLog, PasswordResetRequest, PasswordChangeLog
)
'''
        content = content.replace(insert_marker, correct_import)

        # 写回文件
        with open('admin_panel.py', 'w', encoding='utf-8') as f:
            f.write(content)

        print("✅ 已成功添加models导入语句")
    else:
        print("❌ 找不到插入标记")
        exit(1)
else:
    print("✅ models导入语句已存在")

# 验证
with open('admin_panel.py', 'r', encoding='utf-8') as f:
    content = f.read()
    if 'from models import' in content and 'User,' in content:
        print("✅ 验证成功：导入语句正确")
        # 显示导入部分
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'from models import' in line:
                print("\n当前导入语句：")
                for j in range(i, min(i+8, len(lines))):
                    print(lines[j])
                break
    else:
        print("❌ 验证失败")
        exit(1)
