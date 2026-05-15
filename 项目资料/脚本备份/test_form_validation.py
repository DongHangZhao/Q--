#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试表单验证功能
"""

import os
import sys
from io import BytesIO
from werkzeug.datastructures import FileStorage
from forms import MessageForm
from flask import Flask

def test_message_form_validation():
    """测试MessageForm验证功能"""
    print("测试MessageForm验证功能:")
    
    # 创建一个Flask应用用于测试
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'test-secret-key'
    
    with app.app_context():
        # 测试支持的文件类型
        supported_files = [
            ("test.zip", "application/zip"),
            ("archive.rar", "application/x-rar-compressed"),
            ("archive.tar", "application/x-tar"),
            ("compressed.gz", "application/gzip"),
            ("archive.7z", "application/x-7z-compressed"),
            ("document.pdf", "application/pdf"),
            ("image.jpg", "image/jpeg"),
            ("video.mp4", "video/mp4"),
        ]
        
        for filename, content_type in supported_files:
            print(f"\n测试支持的文件: {filename}")
            
            # 创建文件对象
            file_obj = FileStorage(
                stream=BytesIO(b"fake file content"),
                filename=filename,
                content_type=content_type
            )
            
            # 创建表单实例，模拟表单数据
            form_data = {'content': 'Test message content'}
            files_data = {'attachment': file_obj}
            
            # 使用Flask-WTF推荐的方式创建表单
            form = MessageForm()
            # 直接设置字段值
            form.content.data = form_data['content']
            form.attachment.data = file_obj
            
            # 验证整个表单
            is_valid = form.validate()
            print(f"  表单验证结果: {'✓ 通过' if is_valid else '✗ 失败'}")
            
            if is_valid:
                print(f"  ✓ 文件类型 {filename} 验证通过")
            else:
                print(f"  ✗ 文件类型 {filename} 验证失败")
                for field, errors in form.errors.items():
                    print(f"    {field}: {errors}")
        
        # 测试不支持的文件类型
        unsupported_files = [
            ("malicious.exe", "application/x-executable"),
            ("script.bat", "application/bat"),
            ("dangerous.js", "application/javascript"),
        ]
        
        print(f"\n" + "="*50)
        print("测试不支持的文件类型:")
        
        for filename, content_type in unsupported_files:
            print(f"\n测试不支持的文件: {filename}")
            
            # 创建文件对象
            file_obj = FileStorage(
                stream=BytesIO(b"fake file content"),
                filename=filename,
                content_type=content_type
            )
            
            # 创建表单实例
            form = MessageForm()
            form.content.data = 'Test message content'
            form.attachment.data = file_obj
            
            # 验证表单
            is_valid = form.validate()
            print(f"  表单验证结果: {'✗ 通过(应失败)' if is_valid else '✓ 失败(预期)'}")
            
            if not is_valid and 'attachment' in form.errors:
                print(f"  ✓ 不支持的文件类型被正确拒绝: {form.errors['attachment']}")
            elif not is_valid:
                print(f"  表单错误: {form.errors}")
    
    print("\n表单验证测试完成!")


if __name__ == "__main__":
    test_message_form_validation()