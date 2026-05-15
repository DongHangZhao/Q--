'''
Author: your name
Date: 2026-01-20 22:17:58
LastEditTime: 2026-01-20 22:17:58
LastEditors: your name
Description: In User Settings Edit
FilePath: \Q文件\python_web_project\app_clean.py
'''
# -*- coding: utf-8 -*-
"""
Flask Web Application for Social Platform
"""

from datetime import datetime, timedelta
import sqlite3
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import config
from models import db, User, Post, Video, Comment, Message, News, PostLike, VideoLike, NewsLike, Trending, Follows, UserStatus
from forms import LoginForm, RegistrationForm, ProfileForm, PostForm, VideoForm, MessageForm, NewsForm, AdminUserBanForm, CommentForm
from utils import save_image, save_file, time_ago, calculate_trend_score, generate_avatar_color, generate_filename
import os
import json
from queue import Queue
import threading
from flask import Response
from collections import defaultdict


# 根据环境变量选择配置
config_name = os.environ.get('FLASK_ENV', 'default')
app = Flask(__name__)
app.config.from_object(config[config_name])

# 用于存储SSE连接的队列
user_connections = defaultdict(list)


@app.route('/events')
@login_required
def events():
    """SSE端点，用于推送实时更新"""
    def event_stream():
        # 检查用户是否仍然有效
        if not current_user or not current_user.is_authenticated:
            return

        user_id = current_user.id  # 提前获取用户ID，防止会话变化

        # 为当前用户创建队列
        user_queue = Queue()
        user_connections[user_id].append(user_queue)

        try:
            while True:
                # 检查用户是否仍然有效
                if not current_user or not current_user.is_authenticated:
                    break

                # 等待消息
                message = user_queue.get(timeout=30)  # 30秒超时
                yield f"data: {json.dumps(message)}\n\n"
        except Exception as e:
            print(f"SSE连接异常: {e}")
            return
        finally:
            # 清理连接
            if user_id in user_connections:
                try:
                    user_connections[user_id].remove(user_queue)
                    if not user_connections[user_id]:
                        del user_connections[user_id]
                except ValueError:
                    pass

    # 设置适当的SSE头部
    response = Response(event_stream(), mimetype="text/event-stream")
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['Connection'] = 'keep-alive'
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


def notify_user_status_change(user_id, status_data):
    """通知指定用户的连接有关状态变更的信息"""
    if user_id in user_connections:
        message = {
            'type': 'status_update',
            'user_id': user_id,
            'data': status_data,
            'timestamp': datetime.utcnow().isoformat()
        }

        # 向所有连接广播消息
        for queue in user_connections[user_id]:
            queue.put(message)


def notify_friends_about_status_change(current_user_id, status_data):
    """通知当前用户的所有好友关于状态变更的信息"""
    # 获取当前用户关注的所有用户
    user = User.query.get(current_user_id)
    if user:
        for friend in user.followed:
            if friend.id in user_connections:
                message = {
                    'type': 'friend_status_update',
                    'friend_id': current_user_id,
                    'data': status_data,
                    'timestamp': datetime.utcnow().isoformat()
                }

                # 向好友的所有连接广播消息
                for queue in user_connections[friend.id]:
                    queue.put(message)


# 初始化扩展
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = '请先登录以访问此页面。'


# 初始化数据库
db.init_app(app)


# 创建上传目录
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(os.path.join(UPLOAD_FOLDER, 'avatars')):
    os.makedirs(os.path.join(UPLOAD_FOLDER, 'avatars'))

if not os.path.exists(os.path.join(UPLOAD_FOLDER, 'posts')):
    os.makedirs(os.path.join(UPLOAD_FOLDER, 'posts'))

if not os.path.exists(os.path.join(UPLOAD_FOLDER, 'videos')):
    os.makedirs(os.path.join(UPLOAD_FOLDER, 'videos'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.template_global()
def time_ago(dt):
    """计算时间差，返回多久前的描述"""
    from chinese_time_utils import time_ago as util_time_ago
    return util_time_ago(dt)


@app.template_filter('format_chinese_time')
def format_chinese_time(dt):
    """格式化日期时间为中文显示格式（中国标准时间）"""
    from chinese_time_utils import format_datetime_china
    return format_datetime_china(dt)


# 创建数据库表
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    posts = Post.query.order_by(Post.timestamp.desc()).limit(10).all()
    videos = Video.query.order_by(Video.timestamp.desc()).limit(6).all()
    news_items = News.query.order_by(News.timestamp.desc()).limit(5).all()

    # 获取推荐用户（非当前用户关注的用户）
    suggested_users = []
    online_friends = []
    offline_friends = []

    # 为已登录用户创建发布表单
    form = PostForm() if current_user.is_authenticated else None

    if current_user.is_authenticated:
        # 获取当前用户已关注的用户ID
        following_ids = [f.id for f in current_user.followed]
        # 获取不在关注列表中的用户
        suggested_users = User.query.filter(~User.id.in_(following_ids)).filter(
            User.id != current_user.id).limit(10).all()

        # 获取在线和离线好友
        from sqlalchemy import and_
        # 获取当前用户关注的好友
        followed_users = current_user.followed.all()

        # 清理过期的用户状态
        cleanup_expired_user_statuses()

        for user in followed_users:
            # 获取用户状态
            user_status = UserStatus.query.filter_by(user_id=user.id).first()
            if user_status and user_status.is_online:
                online_friends.append({
                    'user': user,
                    'last_seen': user_status.last_online_time
                })
            else:
                # 如果没有状态记录或离线，查找最后活动时间
                last_seen = user.last_seen or user.join_date
                offline_friends.append({
                    'user': user,
                    'last_seen': last_seen
                })
    else:
        suggested_users = User.query.limit(10).all()

    # 获取今日热度排行
    from chinese_time_utils import calculate_daily_trends
    daily_trends = calculate_daily_trends()

    return render_template('index.html',
                           posts=posts,
                           videos=videos,
                           news_items=news_items,
                           suggested_users=suggested_users,
                           online_friends=online_friends,
                           offline_friends=offline_friends,
                           daily_trends=daily_trends,
                           form=form)


def cleanup_expired_user_statuses():
    """清理长时间未活动的用户状态 - 定期任务"""
    with app.app_context():
        # 将超过2分钟没有更新状态的用户标记为离线
        two_minutes_ago = datetime.utcnow() - timedelta(minutes=2)

        # 查找所有最后活动时间超过2分钟的在线用户
        expired_statuses = UserStatus.query.filter(
            UserStatus.is_online == True,
            UserStatus.last_online_time < two_minutes_ago
        ).all()

        updated_count = 0
        for status in expired_statuses:
            was_online = status.is_online
            status.is_online = False
            status.last_offline_time = datetime.utcnow()

            # 如果用户之前是在线状态，通知其好友
            if was_online:
                user = User.query.get(status.user_id)
                if user:
                    status_change_data = {
                        'user_id': status.user_id,
                        'username': user.username,
                        'is_online': False,
                        'last_seen': time_ago(status.last_offline_time) if status.last_offline_time else '未知时间'
                    }

                    # 通知所有关注该用户的好友
                    notify_friends_about_status_change(
                        status.user_id, status_change_data)

            updated_count += 1

        if updated_count > 0:
            db.session.commit()


# 定期清理过期用户状态
def start_status_cleanup_timer():
    """启动定期清理过期用户状态的定时器"""
    def timer_loop():
        while True:
            try:
                cleanup_expired_user_statuses()
                time.sleep(60)  # 每1分钟清理一次
            except Exception as e:
                print(f"清理用户状态时出错: {e}")
                time.sleep(60)  # 出错后继续等待1分钟再试

    # 启动清理线程
    cleanup_thread = threading.Thread(target=timer_loop, daemon=True)
    cleanup_thread.start()


# 启动状态清理定时器
start_status_cleanup_timer()


if __name__ == '__main__':
    app.run(debug=True)
