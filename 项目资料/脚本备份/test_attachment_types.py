#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试附件类型处理功能
"""

import os
import sys
import tempfile
from io import BytesIO
from werkzeug.datastructures import FileStorage
from utils import save_attachment

def test_attachment_types():
    """测试各种附件类型"""
    print("测试附件类型处理功能:")
    
    # 创建临时上传目录
    test_upload_dir = os.path.join(os.path.dirname(__file__), 'test_attachments')
    if not os.path.exists(test_upload_dir):
        os.makedirs(test_upload_dir)
    
    # 测试各种文件扩展名
    test_files = [
        ("test.zip", b"fake zip content"),
        ("archive.rar", b"fake rar content"), 
        ("document.pdf", b"fake pdf content"),
        ("image.jpg", b"fake jpg content"),
        ("video.mp4", b"fake mp4 content"),
        ("audio.mp3", b"fake mp3 content"),
        ("text.txt", b"fake txt content"),
        ("document.docx", b"fake docx content"),
        ("archive.tar", b"fake tar content"),
        ("compressed.gz", b"fake gz content"),
        ("archive.7z", b"fake 7z content"),
    ]
    
    for filename, content in test_files:
        print(f"\n测试文件: {filename}")
        
        # 创建FileStorage对象模拟上传文件
        file_storage = FileStorage(
            stream=BytesIO(content),
            filename=filename,
            content_type=None
        )
        
        try:
            saved_filename, attachment_type = save_attachment(file_storage, test_upload_dir)
            print(f"  ✓ 成功保存: {saved_filename}")
            print(f"  ✓ 检测类型: {attachment_type}")
            
            # 验证文件确实被保存
            saved_path = os.path.join(test_upload_dir, saved_filename)
            if os.path.exists(saved_path):
                print(f"  ✓ 文件存在: {os.path.getsize(saved_path)} bytes")
                os.remove(saved_path)  # 清理测试文件
            else:
                print(f"  ✗ 文件不存在: {saved_path}")
                
        except Exception as e:
            print(f"  ✗ 错误: {str(e)}")
    
    # 清理测试目录
    try:
        os.rmdir(test_upload_dir)
    except OSError:
        # 如果目录不为空，保留它
        pass
    
    print("\n附件类型测试完成!")


if __name__ == "__main__":
    test_attachment_types()