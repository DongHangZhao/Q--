'''
Author: your name
Date: 2026-01-19 05:37:53
LastEditTime: 2026-01-19 05:37:53
LastEditors: your name
Description: In User Settings Edit
FilePath: \Q文件\项目资料\开发过程文档\测试脚本\test_news_module_fix.py
'''
"""
新闻模块修复验证测试
用于验证AttributeError: 'NewsLike' object has no attribute 'user'问题是否已解决
此测试文件用于记录修复验证过程
"""

from python_web_project.app import app
from python_web_project.models import db, News, User, NewsLike

def test_news_functionality():
    """测试新闻功能"""
    with app.app_context():
        print("开始测试新闻功能修复...")
        
        # 获取所有新闻
        news_items = News.query.all()
        print(f"共找到 {len(news_items)} 条新闻")
        
        if news_items:
            # 测试第一条新闻的点赞用户获取功能
            first_news = news_items[0]
            print(f"测试新闻标题: {first_news.title}")
            
            try:
                # 这是之前出错的方法 - 现在应该正常工作
                liking_users = first_news.get_liking_users()
                print(f"点赞用户数量: {len(liking_users)}")
                
                for user in liking_users:
                    print(f"  - 用户: {user.username}")
                    
                print("✅ get_liking_users() 方法工作正常")
                
            except AttributeError as e:
                print(f"❌ get_liking_users() 方法仍有问题: {e}")
                return False
            
            try:
                # 测试is_liked_by方法
                current_user = User.query.first()  # 模拟当前用户
                if current_user:
                    is_liked = first_news.is_liked_by(current_user)
                    print(f"当前用户是否点赞: {is_liked}")
                    print("✅ is_liked_by() 方法工作正常")
                
            except Exception as e:
                print(f"❌ is_liked_by() 方法有问题: {e}")
                return False
        
        # 测试用户获取新闻点赞功能
        user = User.query.first()
        if user:
            try:
                news_likes = user.get_news_likes()
                print(f"用户 {user.username} 点赞了 {len(news_likes)} 条新闻")
                print("✅ 用户新闻点赞功能工作正常")
            except Exception as e:
                print(f"❌ 用户新闻点赞功能有问题: {e}")
                return False
        
        print("\n🎉 所有新闻功能测试通过！问题已修复。")
        return True

def run_comprehensive_test():
    """运行综合测试"""
    print("="*50)
    print("新闻模块修复验证测试")
    print("="*50)
    
    success = test_news_functionality()
    
    print("="*50)
    if success:
        print("✅ 测试结果: 通过 - 新闻模块功能正常")
    else:
        print("❌ 测试结果: 失败 - 新闻模块存在问题")
    print("="*50)
    
    return success

if __name__ == "__main__":
    run_comprehensive_test()