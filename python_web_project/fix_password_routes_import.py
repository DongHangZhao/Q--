'''
Author: your name
Date: 2026-04-29 17:30:38
LastEditTime: 2026-05-04 22:40:42
LastEditors: ZDH
Description: In User Settings Edit
FilePath: \Q文件\python_web_project\fix_password_routes_import.py
'''
# -*- coding: utf-8 -*-
"""
修复password_routes.py的循环导入问题
"""

# 读取文件
with open('routes/password_routes.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 替换错误的导入
if 'from app import app, db' in content:
    content = content.replace(
        'from app import app, db', 'from models import db')
    print("✅ 已修复循环导入")

    # 写回文件
    with open('routes/password_routes.py', 'w', encoding='utf-8') as f:
        f.write(content)

    print("✅ 文件已保存")
else:
    print("⚠️  未找到需要修复的导入语句")
    print("当前导入部分：")
    with open('routes/password_routes.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i, line in enumerate(lines[14:18], start=15):
            print(f"{i}: {line.rstrip()}")

# 验证
with open('routes/password_routes.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    print("\n验证导入语句：")
    for i, line in enumerate(lines[14:18], start=15):
        print(f"{i}: {line.rstrip()}")

    if 'from app import app, db' in ''.join(lines):
        print("\n❌ 修复失败，仍存在循环导入")
    elif 'from models import db' in ''.join(lines):
        print("\n✅ 修复成功！循环导入已解决")
    else:
        print("\n⚠️  未找到导入语句")
