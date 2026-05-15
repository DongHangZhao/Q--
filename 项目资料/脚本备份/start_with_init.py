'''
Author: your name
Date: 2026-01-10 14:14:18
LastEditTime: 2026-01-10 14:14:18
LastEditors: your name
Description: In User Settings Edit
FilePath: \Q文件\python_web_project\start_with_init.py
'''
"""
咫尺天涯社交平台 - 带数据初始化的启动脚本
"""

import os
import sys
import subprocess
import threading
import time

def initialize_data():
    """初始化数据"""
    print("正在初始化数据...")
    try:
        result = subprocess.run([sys.executable, 'initialize_data.py'], 
                              capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print("数据初始化成功!")
            print(result.stdout)
        else:
            print("数据初始化失败:")
            print(result.stderr)
    except subprocess.TimeoutExpired:
        print("数据初始化超时")

def start_server():
    """启动服务器"""
    print("正在启动服务器...")
    try:
        subprocess.run([sys.executable, 'run.py'])
    except KeyboardInterrupt:
        print("\n服务器已停止")

def main():
    print("咫尺天涯社交平台启动器")
    print("="*40)
    
    # 首先初始化数据
    initialize_data()
    
    print("\n启动服务器，访问 http://localhost:5000")
    print("按 Ctrl+C 停止服务器\n")
    
    # 启动服务器
    start_server()

if __name__ == "__main__":
    main()