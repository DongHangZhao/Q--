#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试附件URL路径处理功能
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_attachment_path_processing():
    """测试附件路径处理逻辑"""
    print("测试附件路径处理功能:")
    
    # 模拟get_attachment_url函数的核心逻辑
    def process_attachment_path(attachment_path):
        if attachment_path:
            # 将系统路径分隔符转换为URL分隔符
            attachment_path = attachment_path.replace('\\', '/')
            
            # 确保路径使用正斜杠
            attachment_path = attachment_path.replace('\\', '/').replace('\\', '/')
            
            # 根据不同情况构建URL
            if attachment_path.startswith('static/'):
                # 如果路径已经包含static，直接使用
                return f"/static/{attachment_path[7:]}"  # 模拟URL
            elif attachment_path.startswith('/'):
                # 如果是绝对路径，去掉开头的'/'并添加static前缀
                return f"/static{attachment_path}"
            elif attachment_path.startswith('uploads/'):
                # 如果以uploads开头，直接使用
                return f"/static/{attachment_path}"
            else:
                # 如果没有static前缀，添加它
                return f"/static/{attachment_path}"
        return None
    
    # 测试不同的路径格式
    test_cases = [
        "uploads\\attachments\\test.jpg",           # Windows风格路径
        "uploads/attachments/test.jpg",             # Unix风格路径
        "static/uploads/attachments/test.jpg",      # 包含static前缀的路径
        "\\uploads\\attachments\\test.jpg",         # 绝对路径风格
        "attachments\\test.jpg",                   # 简单附件路径
        "uploads\\avatars\\user123.png",           # 头像路径
        "uploads/posts/image-test.jpeg",            # 帖子图片路径
    ]
    
    for path in test_cases:
        result = process_attachment_path(path)
        print(f"输入: {path}")
        print(f"输出: {result}")
        print("---")


if __name__ == "__main__":
    test_attachment_path_processing()