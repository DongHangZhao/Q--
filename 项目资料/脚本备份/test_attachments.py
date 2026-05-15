'''
Author: your name
Date: 2026-01-11 19:08:56
LastEditTime: 2026-01-11 19:08:56
LastEditors: your name
Description: In User Settings Edit
FilePath: \Q文件\python_web_project\test_attachments.py
'''
"""
测试附件功能的脚本
"""

import os
import tempfile
from PIL import Image
import sqlite3
from flask_wtf.file import FileAllowed  # 添加缺失的导入


def create_test_files():
    """创建测试文件"""
    print("创建测试文件...")
    
    # 创建测试图片
    img = Image.new('RGB', (100, 100), color='red')
    img.save('test_image.jpg', 'JPEG')
    print("✓ 创建测试图片: test_image.jpg")
    
    # 创建测试压缩包（简单文本文件模拟）
    with open('test_archive.zip', 'w') as f:
        f.write('This is a test archive file')
    print("✓ 创建测试压缩包: test_archive.zip")
    
    # 创建测试文档
    with open('test_document.txt', 'w') as f:
        f.write('This is a test document')
    print("✓ 创建测试文档: test_document.txt")


def test_database_structure():
    """测试数据库结构"""
    print("\n测试数据库结构...")
    
    db_path = os.path.join('database', 'users.db')
    if not os.path.exists(db_path):
        print("✗ 数据库文件不存在")
        return False
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("PRAGMA table_info(messages)")
        columns = [col[1] for col in cursor.fetchall()]
        
        required_cols = ['attachment_path', 'attachment_type', 'attachment_filename']
        missing_cols = [col for col in required_cols if col not in columns]
        
        if missing_cols:
            print(f"✗ 缺少列: {missing_cols}")
            return False
        else:
            print("✓ 所有必需的附件列都存在")
            return True
    except Exception as e:
        print(f"✗ 数据库测试出错: {e}")
        return False
    finally:
        conn.close()


def test_utils_functions():
    """测试工具函数"""
    print("\n测试工具函数...")
    
    try:
        from utils import generate_filename, save_attachment
        
        # 测试文件名生成
        filename = generate_filename("test.jpg")
        if filename.endswith('.jpg') and len(filename) > 10:
            print("✓ generate_filename 函数正常工作")
        else:
            print("✗ generate_filename 函数有问题")
            return False
        
        # 测试附件保存功能（如果测试文件存在）
        if os.path.exists('test_image.jpg'):
            import io
            from werkzeug.datastructures import FileStorage
            
            with open('test_image.jpg', 'rb') as f:
                file_storage = FileStorage(
                    stream=io.BytesIO(f.read()),
                    filename='test_image.jpg',
                    content_type='image/jpeg'
                )
            
            # 重置指针到开始位置
            file_storage.stream.seek(0)
            
            # 测试保存附件
            attachment_folder = 'static/uploads/test_attachments'
            os.makedirs(attachment_folder, exist_ok=True)
            
            saved_filename, attachment_type = save_attachment(file_storage, attachment_folder, max_size=1024*1024*1024)  # 1GB
            
            if attachment_type == 'image' and saved_filename.endswith('.jpg'):
                print("✓ save_attachment 函数正常工作")
                
                # 清理测试文件
                test_file_path = os.path.join(attachment_folder, saved_filename)
                if os.path.exists(test_file_path):
                    os.remove(test_file_path)
                os.rmdir(attachment_folder)
            else:
                print(f"✗ save_attachment 函数有问题: type={attachment_type}, filename={saved_filename}")
                return False
        
        return True
    except Exception as e:
        print(f"✗ 工具函数测试出错: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_form_validation():
    """测试表单验证"""
    print("\n测试表单验证...")
    
    try:
        from forms import MessageForm
        from flask import Flask
        
        # 创建一个简单的Flask应用用于测试
        app = Flask(__name__)
        app.config['WTF_CSRF_ENABLED'] = False  # 禁用CSRF以进行测试
        app.config['SECRET_KEY'] = 'test-secret-key'
        
        with app.test_request_context(method='POST', data={}):
            form = MessageForm()
            
            # 检查attachment字段是否存在
            if hasattr(form, 'attachment'):
                print("✓ MessageForm 包含 attachment 字段")
                
                # 检查验证器 - 验证器类型
                attachment_validators = form.attachment.validators
                has_file_allowed = any(isinstance(v, FileAllowed) for v in attachment_validators)
                
                if has_file_allowed:
                    print("✓ MessageForm attachment 字段包含 FileAllowed 验证器")
                else:
                    print("✗ MessageForm attachment 字段缺少 FileAllowed 验证器")
                    return False
            else:
                print("✗ MessageForm 不包含 attachment 字段")
                return False
        
        return True
    except Exception as e:
        print(f"✗ 表单验证测试出错: {e}")
        import traceback
        traceback.print_exc()
        return False


def cleanup_test_files():
    """清理测试文件"""
    print("\n清理测试文件...")
    
    test_files = ['test_image.jpg', 'test_archive.zip', 'test_document.txt']
    for file in test_files:
        if os.path.exists(file):
            os.remove(file)
            print(f"  删除: {file}")


def main():
    """主测试函数"""
    print("=" * 60)
    print("测试附件功能改进")
    print("=" * 60)
    
    # 创建测试文件
    create_test_files()
    
    # 运行各项测试
    tests = [
        ("数据库结构", test_database_structure),
        ("工具函数", test_utils_functions),
        ("表单验证", test_form_validation),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n运行 {test_name} 测试...")
        result = test_func()
        results.append((test_name, result))
    
    # 输出测试结果
    print("\n" + "=" * 60)
    print("测试结果汇总:")
    print("=" * 60)
    
    all_passed = True
    for test_name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n🎉 所有测试通过！附件功能已正确实现。")
    else:
        print("\n⚠️  有些测试失败，请检查实现。")
    
    # 清理测试文件
    cleanup_test_files()
    
    print("\n测试完成！")


if __name__ == "__main__":
    main()




