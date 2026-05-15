'''
Author: your name
Date: 2026-01-11 18:56:47
LastEditTime: 2026-01-11 18:56:47
LastEditors: your name
Description: In User Settings Edit
FilePath: \Q文件\python_web_project\verify_improvements.py
'''
"""
验证项目改进的脚本
此脚本验证：
1. 附件功能是否正常工作
2. 时间戳是否正确设置
3. 模板中的附件显示是否正确
"""

import os
import sys
sys.path.append('.')

from datetime import datetime
from app import app, db, Message, User
from utils import generate_filename

def verify_improvements():
    print("="*60)
    print("验证项目改进")
    print("="*60)
    
    # 1. 验证数据库表结构
    print("\n1. 验证数据库表结构...")
    with app.app_context():
        # 检查Message模型是否包含附件字段
        columns = db.inspect(db.engine).get_columns('messages')
        column_names = [col['name'] for col in columns]
        
        required_attachment_fields = ['attachment_path', 'attachment_type', 'attachment_filename']
        missing_fields = [field for field in required_attachment_fields if field not in column_names]
        
        if not missing_fields:
            print("   ✓ 所有附件字段已存在")
        else:
            print(f"   ✗ 缺少字段: {missing_fields}")
            return False
    
    # 2. 验证时间戳功能
    print("\n2. 验证时间戳功能...")
    try:
        # 检查Message模型的timestamp字段
        timestamp_column = None
        for col in columns:
            if col['name'] == 'timestamp':
                timestamp_column = col
                break
        
        if timestamp_column and 'DATETIME' in str(timestamp_column['type']):
            print("   ✓ 时间戳字段类型正确")
        else:
            print("   ✗ 时间戳字段存在问题")
            return False
    except Exception as e:
        print(f"   ✗ 时间戳验证出错: {e}")
        return False
    
    # 3. 验证模板文件中的附件显示功能
    print("\n3. 验证模板文件...")
    
    # 检查chat_window.html中的附件显示功能
    with open('templates/chat_window.html', 'r', encoding='utf-8') as f:
        chat_content = f.read()
    
    if 'attachment-preview' in chat_content and 'video controls' in chat_content:
        print("   ✓ chat_window.html中的附件显示功能已更新")
    else:
        print("   ✗ chat_window.html中的附件显示功能未正确更新")
        return False
    
    # 检查messages.html中的附件显示功能
    with open('templates/messages.html', 'r', encoding='utf-8') as f:
        messages_content = f.read()
    
    if 'attachment-preview' in messages_content and 'video controls' in messages_content:
        print("   ✓ messages.html中的附件显示功能已更新")
    else:
        print("   ✗ messages.html中的附件显示功能未正确更新")
        return False
    
    # 4. 验证JavaScript功能
    if 'openImageModal' in chat_content and 'openImageModal' in messages_content:
        print("   ✓ 图片模态框功能已添加")
    else:
        print("   ✗ 图片模态框功能未正确添加")
        return False
    
    # 5. 验证时间处理改进
    print("\n4. 验证时间处理改进...")
    with open('app.py', 'r', encoding='utf-8') as f:
        app_content = f.read()
    
    if 'datetime.now()' in app_content and 'timestamp=datetime.now()' in app_content:
        print("   ✓ 时间戳处理已更新为使用当前时间")
    else:
        print("   ✗ 时间戳处理未正确更新")
        return False
    
    print("\n" + "="*60)
    print("✅ 所有改进验证通过！")
    print("项目现在具备以下改进功能：")
    print("   • 私信支持图片、视频、音频等多种附件类型")
    print("   • 附件可在网页中直接预览和播放")
    print("   • 支持点击图片查看大图模式")
    print("   • 消息时间戳使用真实时间")
    print("   • 视频和音频可在聊天窗口中直接播放")
    print("="*60)
    
    return True

if __name__ == "__main__":
    verify_improvements()