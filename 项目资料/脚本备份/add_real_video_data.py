'''
Author: your name
Date: 2026-01-11 01:18:07
LastEditTime: 2026-01-11 01:18:08
LastEditors: your name
Description: In User Settings Edit
FilePath: \Q文件\python_web_project\add_real_video_data.py
'''
"""
Author: your name
Date: 2026-01-11 01:11:18
LastEditTime: 2026-01-11 01:11:18
LastEditors: your name
Description: In User Settings Edit
FilePath: \\Q文件\\python_web_project\\add_real_video_data.py
"""

"""
为内置用户添加真实的短视频数据，使用来自国内视频网站的短视频链接
"""
from app import app, db
from models import User, Video, Comment
from datetime import datetime, timedelta
import random
import time
from zoneinfo import ZoneInfo  # Python 3.9+


def add_real_video_data():
    """为内置用户添加真实的视频数据"""
    with app.app_context():
        # 内置用户名列表
        builtin_users = ['admin', 'tianmi', 'FallPetal', 'zhangsan', 'lisi', 'xiaoming', 'zhaoliu', 'wangwu', 'meimei']
        
        # 来自国内视频网站的真实短视频链接（使用公共测试链接）
        real_video_urls = [
            "https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_1mb.mp4",  # 公共测试视频
            "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",  # 开源视频
            "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4",  # 开源视频
            "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",  # 开源视频
            "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4",  # 开源视频
            "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4",  # 开源视频
            "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4",  # 开源视频
            "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerMeltdowns.mp4",  # 开源视频
            "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4",  # 开源视频
        ]
        
        # 来自国内视频网站的短视频链接（模拟真实情况）
        domestic_video_urls = [
            "https://vdse.bdstatic.com//7cc64f3c1b7e5ef0fa117ad52309b119.mp4?authorization=bce-auth-v1/3aa752ea7e4140a5a37363e34c4b4ac1/2024-01-11T00:00:00Z/86400/3aa752ea7e4140a5a37363e34c4b4ac1/648542812e32543391810250e8e545920482890702495149436443072149058",  # 示例链接（实际不可用，仅作演示）
            "https://aweme.snssdk.com/aweme/v1/playwm/?video_id=v0200fg10000cbk6gjcabfuq7hu3n8lg&ratio=720p&line=0",  # 抖音示例（实际不可用，仅作演示）
        ]
        
        # 结合使用真实可访问的链接和模拟的国内视频链接
        all_video_urls = real_video_urls[:len(builtin_users)]  # 确保每个用户都有一个视频链接
        
        # 视频标题列表
        video_titles = [
            "日常生活片段",
            "美食制作教程",
            "风景旅游分享",
            "萌宠可爱瞬间",
            "健身运动指南",
            "手工DIY技巧",
            "音乐才艺展示",
            "搞笑趣事分享",
            "知识科普小课堂"
        ]
        
        # 视频描述列表
        video_descriptions = [
            "分享日常生活中的有趣片段，记录美好时光。",
            "简单易学的美食制作教程，让你在家也能做出美味佳肴。",
            "美丽的风景旅游分享，带你云游世界。",
            "可爱的萌宠瞬间，治愈你的心灵。",
            "科学的健身运动指南，帮助你保持健康体魄。",
            "实用的手工DIY技巧，激发你的创造力。",
            "精彩的音乐才艺展示，享受美妙旋律。",
            "有趣的搞笑趣事分享，让你开怀大笑。",
            "简洁明了的知识科普，拓宽你的视野。"
        ]
        
        # 评论内容列表
        comment_contents = [
            "视频很棒！👍",
            "学到了很多，感谢分享！",
            "拍得真好，已点赞！",
            "期待更多优质内容！",
            "很有意思，已收藏！",
            "制作精良，大力支持！",
            "看完心情愉悦！",
            "非常有用的信息，感谢！",
            "拍摄技术不错，继续加油！",
            "强烈推荐，值得一看！",
            "内容很丰富，收获颇丰！",
            "视频质量很高，清晰流畅！",
            "很喜欢这种风格的内容！",
            "坐等更新，不要鸽哦！",
            "受益匪浅，谢谢博主！",
            "转发了，朋友们都说好！",
            "太有意思了，笑死我了！",
            "干货满满，收藏慢慢看！",
            "技术流，学习了！",
            "感动哭了，太温暖了！"
        ]
        
        # 为每个内置用户创建视频
        for i, username in enumerate(builtin_users):
            user = User.query.filter_by(username=username).first()
            if user:
                # 选择标题和描述
                title_idx = i % len(video_titles)
                title = f"{video_titles[title_idx]} - {username}"
                description = f"{video_descriptions[title_idx]} 这是用户{username}分享的精彩内容。"
                
                # 选择视频链接
                video_url = all_video_urls[i % len(all_video_urls)]
                
                # 生成过去几天到几周内的随机时间戳（模拟真实上传时间）
                now = datetime.now(ZoneInfo("Asia/Shanghai"))
                upload_time = now - timedelta(days=random.randint(1, 21), hours=random.randint(0, 23), minutes=random.randint(0, 59))
                
                # 检查是否已存在该用户的视频
                existing_video = Video.query.filter_by(title=title).first()
                if not existing_video:
                    # 创建视频记录
                    video = Video(
                        title=title,
                        description=description,
                        video_url=video_url,
                        thumbnail_url="",  # 将稍后处理缩略图
                        uploader=user,
                        views=random.randint(100, 10000),  # 随机观看次数
                        likes_count=random.randint(10, 500),  # 随机点赞数
                        timestamp=upload_time  # 使用真实的时间戳
                    )
                    
                    db.session.add(video)
                    db.session.flush()  # 获取视频ID以便创建评论
                    
                    # 为视频创建一些评论（使用真实时间戳）
                    num_comments = random.randint(3, 8)
                    for j in range(num_comments):
                        # 随机选择一个用户作为评论者（可以是其他内置用户）
                        comment_users = User.query.all()
                        comment_user = random.choice(comment_users)
                        
                        comment_content = random.choice(comment_contents)
                        
                        # 生成评论时间戳（在视频上传之后的时间内随机生成）
                        comment_time = upload_time + timedelta(hours=random.randint(0, 72), minutes=random.randint(0, 59))
                        
                        # 确保评论时间不超过当前时间
                        if comment_time > now:
                            comment_time = now - timedelta(minutes=random.randint(1, 60))
                        
                        comment = Comment(
                            content=comment_content,
                            author=comment_user,
                            video=video,
                            timestamp=comment_time  # 使用真实的时间戳
                        )
                        
                        db.session.add(comment)
                    
                    print(f"为用户 {username} 创建视频: {title} (上传时间: {upload_time.strftime('%Y-%m-%d %H:%M:%S')})，包含 {num_comments} 条评论")
                else:
                    print(f"用户 {username} 的视频 {title} 已存在，跳过创建")
        
        db.session.commit()
        print("真实的视频数据添加完成")


if __name__ == '__main__':
    add_real_video_data()