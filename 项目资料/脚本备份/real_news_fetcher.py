'''
Author: your name
Date: 2026-01-19 03:44:17
LastEditTime: 2026-01-19 03:44:17
LastEditors: your name
Description: In User Settings Edit
FilePath: \Q文件\python_web_project\real_news_fetcher.py
'''
'''
Author: your name
Date: 2026-01-19 04:00:00
LastEditTime: 2026-01-19 04:00:00
LastEditors: your name
Description: 获取真实新闻数据的脚本
FilePath: \Q文件\python_web_project\real_news_fetcher.py
'''

"""
真实新闻数据获取脚本
使用RSS源获取真实的新闻数据
"""

import feedparser
import requests
from datetime import datetime, timezone
from app import app, db
from models import News
import re


def clean_html(html_content):
    """清理HTML标签"""
    if not html_content:
        return ""
    # 移除HTML标签
    clean_text = re.sub('<[^<]+?>', '', html_content)
    return clean_text.strip()


def fetch_news_from_rss():
    """从RSS源获取真实新闻"""
    # 使用一些公开的RSS新闻源
    rss_feeds = [
        'http://news.baidu.com/n?cmd=file&format=rss&tn=rss',
        'https://www.zaobao.com.sg/special/feed/rss',
        'https://cn.nytimes.com/rss/',
        # 更多RSS源可以添加
    ]
    
    all_news = []
    
    for feed_url in rss_feeds:
        try:
            print(f"正在获取RSS源: {feed_url}")
            feed = feedparser.parse(feed_url)
            
            if feed.bozo:  # 检查是否有解析错误
                print(f"RSS源解析可能有问题: {feed_url}")
                
            for entry in feed.entries[:5]:  # 只取前5条新闻
                try:
                    title = entry.get('title', '无标题')
                    content = clean_html(entry.get('summary', entry.get('description', '')))
                    link = entry.get('link', '')
                    
                    # 获取发布日期
                    pub_date = None
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        pub_date = datetime(*entry.published_parsed[:6])
                    elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                        pub_date = datetime(*entry.updated_parsed[:6])
                    else:
                        pub_date = datetime.now()
                    
                    # 获取源名称
                    source = feed.feed.get('title', '未知来源')
                    
                    # 获取图片（如果有的话）
                    image_url = None
                    if hasattr(entry, 'media_content') and entry.media_content:
                        image_url = entry.media_content[0].get('url', None)
                    elif hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
                        image_url = entry.media_thumbnail[0].get('url', None)
                    elif hasattr(entry, 'links'):
                        for link_obj in entry.links:
                            if link_obj.get('type', '').startswith('image/'):
                                image_url = link_obj.href
                                break
                    
                    # 如果没有图片，使用占位图
                    if not image_url:
                        image_url = f'https://via.placeholder.com/600x400/4a90e2/ffffff?text={title[:20]}'
                    
                    # 生成摘要
                    summary = content[:100] + "..." if len(content) > 100 else content
                    
                    news_item = {
                        'title': title,
                        'content': content,
                        'summary': summary,
                        'image_url': image_url,
                        'source': source,
                        'timestamp': pub_date
                    }
                    
                    all_news.append(news_item)
                    
                except Exception as e:
                    print(f"处理RSS条目时出错: {e}")
                    continue
                    
        except Exception as e:
            print(f"获取RSS源失败 {feed_url}: {e}")
            continue
    
    return all_news


def fetch_news_from_api():
    """从免费新闻API获取新闻（如果有API密钥的话）"""
    # 这是一个示例，实际使用时需要替换为有效的API密钥
    # 例如使用NewsAPI: https://newsapi.org/
    # 或其他提供免费额度的新闻API
    
    # 由于没有实际的API密钥，我们使用RSS作为主要数据源
    # 但这里展示如何实现API调用
    try:
        # 示例代码（需要实际的API密钥）
        # api_key = "YOUR_API_KEY_HERE"
        # url = f"https://newsapi.org/v2/top-headlines?country=cn&apiKey={api_key}"
        # response = requests.get(url)
        # data = response.json()
        # return parse_api_response(data)
        
        # 暂时返回空列表，因为没有API密钥
        return []
    except Exception as e:
        print(f"API请求失败: {e}")
        return []


def update_real_news():
    """更新真实新闻数据"""
    print(f"[{datetime.now()}] 开始获取真实新闻数据...")
    
    with app.app_context():
        # 从RSS源获取新闻
        rss_news = fetch_news_from_rss()
        # api_news = fetch_news_from_api()  # 暂时不用API，因为需要密钥
        
        all_news = rss_news  # + api_news
        
        if not all_news:
            print("未能获取到任何新闻数据")
            return
        
        print(f"获取到 {len(all_news)} 条新闻")
        
        # 插入或更新新闻数据
        for news_item in all_news:
            # 检查是否已存在相同的新闻（基于标题和源）
            existing_news = News.query.filter_by(
                title=news_item['title'],
                source=news_item['source']
            ).first()
            
            if existing_news:
                # 更新现有新闻
                existing_news.content = news_item['content']
                existing_news.summary = news_item['summary']
                existing_news.image_url = news_item['image_url']
                existing_news.timestamp = news_item['timestamp']
                print(f"更新新闻: {news_item['title'][:50]}...")
            else:
                # 创建新新闻
                news = News(
                    title=news_item['title'],
                    content=news_item['content'],
                    summary=news_item['summary'],
                    image_url=news_item['image_url'],
                    source=news_item['source'],
                    timestamp=news_item['timestamp']
                )
                db.session.add(news)
                print(f"添加新闻: {news_item['title'][:50]}...")
        
        try:
            db.session.commit()
            print(f"[{datetime.now()}] 成功更新了 {len(all_news)} 条新闻")
        except Exception as e:
            print(f"[{datetime.now()}] 更新新闻时出错: {e}")
            db.session.rollback()


if __name__ == "__main__":
    with app.app_context():
        update_real_news()