'''
Author: your name
Date: 2026-01-11 01:11:18
LastEditTime: 2026-01-11 01:11:18
LastEditors: your name
Description: In User Settings Edit
FilePath: \Q文件\python_web_project\add_complete_video_data.py
'''
"""
为内置用户添加完整的模拟短视频数据，包括视频、缩略图和评论
"""
from app import app, db
from models import User, Video, Comment
import os
import random
from datetime import datetime, timedelta


def add_complete_video_data():
    """为内置用户添加完整的视频数据"""
    with app.app_context():
        # 创建视频目录
        videos_dir = 'static/uploads/videos'
        if not os.path.exists(videos_dir):
            os.makedirs(videos_dir)
        
        # 创建缩略图目录
        thumbs_dir = os.path.join(videos_dir)
        if not os.path.exists(thumbs_dir):
            os.makedirs(thumbs_dir)
        
        # 内置用户名列表
        builtin_users = ['admin', 'tianmi', 'FallPetal', 'zhangsan', 'lisi', 'xiaoming', 'zhaoliu', 'wangwu', 'meimei']
        
        # 视频标题列表
        video_titles = [
            "日常生活的有趣瞬间",
            "美食制作教程",
            "旅游风光欣赏",
            "宠物萌宠时刻",
            "运动健身指导",
            "手工DIY教程",
            "音乐表演分享",
            "搞笑段子集锦",
            "知识科普讲解"
        ]
        
        # 视频描述列表
        video_descriptions = [
            "分享日常生活中的有趣瞬间，感受平凡中的美好。",
            "教你制作简单又美味的家常菜。",
            "带你领略祖国大好河山的壮丽景色。",
            "可爱的宠物们带来的欢乐时光。",
            "专业的运动健身指导，帮助你保持健康。",
            "简单易学的手工DIY教程，发挥创意。",
            "精彩的音乐表演，陶冶情操。",
            "轻松愉快的搞笑段子，放松心情。",
            "有趣的知识科普，增长见识。"
        ]
        
        # 评论内容列表
        comment_contents = [
            "很棒的视频！",
            "学到了很多，谢谢分享！",
            "拍得真好，点赞！",
            "期待更多优质内容！",
            "很有意思，收藏了！",
            "制作精良，支持！",
            "看完心情很好！",
            "有用的信息，感谢！",
            "拍得不错，继续加油！",
            "推荐观看，值得一看！",
            "内容很丰富，学到不少！",
            "视频质量很高！",
            "很喜欢这种风格！",
            "期待更新！",
            "受益匪浅，谢谢！"
        ]
        
        # 为每个内置用户创建视频
        for i, username in enumerate(builtin_users):
            user = User.query.filter_by(username=username).first()
            if user:
                # 选择标题和描述
                title_idx = i % len(video_titles)
                title = f"{video_titles[title_idx]} - {username}"
                description = f"{video_descriptions[title_idx]} 这是用户{username}分享的精彩内容。"
                
                # 创建缩略图文件名
                thumb_filename = f"thumb_{i+1}.jpg"
                thumb_filepath = os.path.join(thumbs_dir, thumb_filename)
                
                # 创建视频文件名
                video_filename = f"video_{i+1}.mp4"
                video_filepath = os.path.join(videos_dir, video_filename)
                
                # 创建虚拟缩略图和视频文件
                with open(video_filepath, 'w') as f:
                    f.write(f"Virtual video file for {title}")
                
                with open(thumb_filepath, 'w') as f:
                    f.write(f"Virtual thumbnail for {title}")
                
                # 检查是否已存在该用户的视频
                existing_video = Video.query.filter_by(title=title).first()
                if not existing_video:
                    # 创建视频记录
                    video = Video(
                        title=title,
                        description=description,
                        video_url=f"uploads/videos/{video_filename}",
                        thumbnail_url=f"uploads/videos/{thumb_filename}",  # 使用虚拟缩略图
                        uploader=user,
                        views=random.randint(100, 10000),  # 随机观看次数
                        likes_count=random.randint(10, 500)  # 随机点赞数
                    )
                    
                    db.session.add(video)
                    db.session.flush()  # 获取视频ID以便创建评论
                    
                    # 为视频创建一些评论
                    num_comments = random.randint(3, 8)
                    for j in range(num_comments):
                        # 随机选择一个用户作为评论者（可以是其他内置用户）
                        comment_user = random.choice(User.query.all())
                        
                        comment_content = random.choice(comment_contents)
                        comment_time = datetime.utcnow() - timedelta(days=random.randint(0, 30))
                        
                        comment = Comment(
                            content=comment_content,
                            author=comment_user,
                            video=video,
                            timestamp=comment_time
                        )
                        
                        db.session.add(comment)
                    
                    print(f"为用户 {username} 创建视频: {title}，包含 {num_comments} 条评论")
        
        db.session.commit()
        print("完整的视频数据添加完成")


if __name__ == '__main__':
    add_complete_video_data()