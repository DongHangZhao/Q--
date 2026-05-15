'''
Author: your name
Date: 2026-01-10 13:04:26
LastEditTime: 2026-01-10 13:04:26
LastEditors: your name
Description: In User Settings Edit
FilePath: e:/办公练习/Html/Q文件/python_web_project/test_app.py
'''
"""
Python Web项目测试文件
用于测试应用程序的基本功能
"""

import unittest
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        """设置测试客户端"""
        self.app = app
        self.client = self.app.test_client()
        
    def test_home_page(self):
        """测试首页"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Python Web项目'.encode('utf-8'), response.data)
        
    def test_users_page(self):
        """测试用户页面"""
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertIn('用户管理系统'.encode('utf-8'), response.data)
        
    def test_about_page(self):
        """测试关于页面"""
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn('关于我们'.encode('utf-8'), response.data)
        
    def test_api_users_get(self):
        """测试API获取用户"""
        response = self.client.get('/api/users')
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/json', response.content_type)

if __name__ == '__main__':
    print("运行Python Web项目测试...")
    unittest.main()