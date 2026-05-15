'''
Author: your name
Date: 2026-04-11 23:15:34
LastEditTime: 2026-04-11 23:15:34
LastEditors: your name
Description: In User Settings Edit
FilePath: \Q文件\python_web_project\fix_trending.py
'''
# -*- coding: utf-8 -*-
"""
修复Trending表的date字段并重新计算热度
"""

import os
import sys
from datetime import datetime, date
from models import Trending
from app import app, db

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def fix_trending_dates():
    """修复Trending表的日期字段"""

    print("="*70)
    print("修复Trending表日期字段")
    print("="*70)

    with app.app_context():
        # 方案1：删除所有Trending记录，重新插入
        print("\n清空Trending表...")
        Trending.query.delete()
        db.session.commit()
        print("已清空")

        print("\n现在请运行: python update_trending.py")
        print("注意：需要在update_trending.py中将date字段改为date类型")


if __name__ == '__main__':
    fix_trending_dates()
