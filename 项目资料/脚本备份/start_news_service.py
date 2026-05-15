'''
Author: your name
Date: 2026-01-19 03:09:57
LastEditTime: 2026-01-19 03:09:57
LastEditors: your name
Description: In User Settings Edit
FilePath: \Q文件\python_web_project\start_news_service.py
'''
'''
Author: your name
Date: 2026-01-19 03:45:00
LastEditTime: 2026-01-19 03:45:00
LastEditors: your name
Description: 启动新闻和热度服务
FilePath: \Q文件\python_web_project\start_news_service.py
'''

"""
启动新闻和热度服务
这个脚本将启动后台服务来定期更新新闻和热度排行
"""

import os
import sys
from threading import Thread
import time
from datetime import datetime
from scrape_news import update_daily_news
from calculate_trending import calculate_daily_trending
import schedule

def run_news_and_trending_service():
    """
    运行新闻和热度服务
    """
    print(f"[{datetime.now()}] 启动新闻和热度后台服务...")
    
    # 设置每日更新任务
    schedule.every().day.at("00:00").do(update_daily_news)  # 每天午夜更新新闻
    schedule.every().day.at("00:05").do(calculate_daily_trending)  # 每天00:05计算热度排行
    
    # 为了测试目的，也可以设置更频繁的任务
    # schedule.every(10).minutes.do(update_daily_news)  # 每10分钟更新新闻
    # schedule.every(15).minutes.do(calculate_daily_trending)  # 每15分钟计算热度排行
    
    print("已设置定时任务:")
    print("- 每天午夜00:00更新新闻")
    print("- 每天凌晨00:05计算热度排行")
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # 每分钟检查一次


def start_services():
    """
    启动服务
    """
    # 在单独的线程中运行服务
    service_thread = Thread(target=run_news_and_trending_service, daemon=True)
    service_thread.start()
    
    print("新闻和热度服务已启动")
    
    # 保持主线程运行
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n收到退出信号，正在关闭服务...")
        sys.exit(0)


if __name__ == "__main__":
    start_services()