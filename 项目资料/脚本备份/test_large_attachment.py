#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试大附件上传功能（最大1GB）
"""

import os
import sys
from io import BytesIO
from werkzeug.datastructures import FileStorage
from utils import save_attachment

def test_large_attachment_limit():
    """测试大附件上传限制"""
    print("测试大附件上传功能（最大1GB）:")
    
    # 创建临时上传目录
    test_upload_dir = os.path.join(os.path.dirname(__file__), 'test_large_attachments')
    if not os.path.exists(test_upload_dir):
        os.makedirs(test_upload_dir)
    
    # 测试不同大小的文件
    test_sizes = [
        ("small_file.txt", 1024),                    # 1KB
        ("medium_file.zip", 10 * 1024 * 1024),      # 10MB
        ("large_file.pdf", 100 * 1024 * 1024),      # 100MB
        ("very_large_file.tar", 500 * 1024 * 1024), # 500MB
    ]
    
    for filename, size in test_sizes:
        print(f"\n测试文件: {filename} ({size / (1024*1024):.2f} MB)")
        
        # 创建指定大小的测试内容
        content = b'0' * 1024  # 只创建1KB的内容并重复以模拟大文件大小
        # 我们实际上不创建完整的大型内容，而是测试大小检查逻辑
        # 通过修改file_storage的tell方法来模拟大文件大小
        
        # 创建一个自定义的流来模拟大文件
        class LargeFileStream:
            def __init__(self, size):
                self.size = size
                self.pos = 0
                
            def seek(self, offset, whence=0):
                if whence == 0:  # SEEK_SET
                    self.pos = offset
                elif whence == 1:  # SEEK_CUR
                    self.pos += offset
                elif whence == 2:  # SEEK_END
                    self.pos = self.size + offset
                return self.pos
                
            def tell(self):
                return self.pos
                
            def read(self, size=-1):
                if size == -1:
                    size = self.size - self.pos
                end_pos = min(self.pos + size, self.size)
                read_size = end_pos - self.pos
                self.pos = end_pos
                return b'0' * read_size
                
            def write(self, data):
                pass  # 简单实现，不需要写入

        large_stream = LargeFileStream(size)
        
        # 创建FileStorage对象模拟上传文件
        file_storage = FileStorage(
            stream=large_stream,
            filename=filename,
            content_type='application/octet-stream'
        )
        
        try:
            saved_filename, attachment_type = save_attachment(file_storage, test_upload_dir)
            print(f"  ✓ 成功保存: {saved_filename}")
            print(f"  ✓ 检测类型: {attachment_type}")
            
            # 验证文件确实被保存
            saved_path = os.path.join(test_upload_dir, saved_filename)
            if os.path.exists(saved_path):
                saved_size = os.path.getsize(saved_path)
                print(f"  ✓ 文件已保存: {saved_size / (1024*1024):.2f} MB")
                os.remove(saved_path)  # 清理测试文件
            else:
                print(f"  ✗ 文件不存在: {saved_path}")
                
        except Exception as e:
            print(f"  ✗ 错误: {str(e)}")
    
    # 测试超过1GB的文件（应该失败）
    print(f"\n测试超大文件 (>1GB, 应该失败):")
    oversized_filename = "oversized_file.dat"
    oversized_size = 2 * 1024 * 1024 * 1024  # 2GB
    
    print(f"测试文件: {oversized_filename} ({oversized_size / (1024*1024*1024):.2f} GB)")
    
    # 创建一个模拟超大文件的流
    class OversizeFileStream:
        def __init__(self, size):
            self.size = size
            self.pos = 0
            
        def seek(self, offset, whence=0):
            if whence == 0:  # SEEK_SET
                self.pos = offset
            elif whence == 1:  # SEEK_CUR
                self.pos += offset
            elif whence == 2:  # SEEK_END
                self.pos = self.size + offset
            return self.pos
            
        def tell(self):
            return self.pos
            
        def read(self, size=-1):
            if size == -1:
                size = self.size - self.pos
            end_pos = min(self.pos + size, self.size)
            read_size = end_pos - self.pos
            self.pos = end_pos
            return b'0' * read_size
            
        def write(self, data):
            pass  # 简单实现，不需要写入

    oversized_stream = OversizeFileStream(oversized_size)
    
    # 创建FileStorage对象模拟上传文件
    file_storage = FileStorage(
        stream=oversized_stream,
        filename=oversized_filename,
        content_type='application/octet-stream'
    )
    
    try:
        saved_filename, attachment_type = save_attachment(file_storage, test_upload_dir)
        print(f"  ✗ 意外成功保存: {saved_filename} (这不应该发生!)")
        
    except ValueError as e:
        if "文件过大" in str(e):
            print(f"  ✓ 正确拒绝超大文件: {str(e)}")
        else:
            print(f"  ? 其他错误: {str(e)}")
    except Exception as e:
        print(f"  ? 其他异常: {str(e)}")
    
    # 清理测试目录
    try:
        os.rmdir(test_upload_dir)
    except OSError:
        # 如果目录不为空，保留它
        pass
    
    print("\n大附件上传测试完成!")


if __name__ == "__main__":
    test_large_attachment_limit()