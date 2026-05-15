'''
Author: your name
Date: 2026-01-11 00:50:09
LastEditTime: 2026-01-11 00:50:09
LastEditors: your name
Description: In User Settings Edit
FilePath: \Q文件\python_web_project\download_avatars.py
'''
"""
下载头像图片到本地
"""
import os
import requests
from urllib.parse import urlparse


def download_avatar_images():
    """下载头像图片到本地uploads/avatars目录"""
    
    # 创建avatars目录
    avatars_dir = 'static/uploads/avatars'
    if not os.path.exists(avatars_dir):
        os.makedirs(avatars_dir)
    
    # 定义头像URL列表
    avatar_urls = [
        "https://ui-avatars.com/api/?name=admin&background=random&size=200",
        "https://ui-avatars.com/api/?name=tianmi&background=random&size=200", 
        "https://ui-avatars.com/api/?name=FallPetal&background=random&size=200",
        "https://ui-avatars.com/api/?name=zhangsan&background=random&size=200",
        "https://ui-avatars.com/api/?name=lisi&background=random&size=200",
        "https://ui-avatars.com/api/?name=Default1&background=random&size=200",
        "https://ui-avatars.com/api/?name=Default2&background=random&size=200",
        "https://ui-avatars.com/api/?name=Default3&background=random&size=200",
        "https://ui-avatars.com/api/?name=Default4&background=random&size=200",
        "https://ui-avatars.com/api/?name=Default5&background=random&size=200"
    ]
    
    for i, url in enumerate(avatar_urls):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                # 生成文件名
                filename = f"avatar_{i+1}.png"
                filepath = os.path.join(avatars_dir, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                print(f"下载头像 {filename} 成功")
            else:
                print(f"下载头像失败: {url}")
        except Exception as e:
            print(f"下载头像出错 {url}: {str(e)}")
    
    print("头像下载完成")


if __name__ == '__main__':
    download_avatar_images()