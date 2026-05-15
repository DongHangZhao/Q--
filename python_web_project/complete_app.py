'''
Author: your name
Date: 2026-01-20 23:08:00
LastEditTime: 2026-01-20 23:08:00
LastEditors: your name
Description: In User Settings Edit
FilePath: \Q文件\python_web_project\complete_app.py
'''
'''
Author: your name
Date: 2026-01-20 22:17:58
LastEditTime: 2026-01-20 22:29:33
LastEditors: ZDH
Description: In User Settings Edit
FilePath: \Q文件\python_web_project\app_clean.py
'''
# -*- coding: utf-8 -*-
"""
Flask Web Application for Social Platform
"""

from collections import defaultdict
from flask import Response
import threading
from queue import Queue
import json
import os
from utils import save_image, save_file, time_ago, calculate_trend_score, generate_avatar_color, generate_filename
from forms import LoginForm, RegistrationForm, ProfileForm, PostForm, VideoForm, MessageForm, NewsForm, AdminUserBanForm, CommentForm
from models import db, User, Post, Video, Comment, Message, News, PostLike, VideoLike, NewsLike, Trending, Follows, UserStatus
from config import config
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
import time
from datetime import datetime, timedelta
import sqlite3


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


@app.template_global()
def get_avatar_url(avatar_filename):
    """获取头像URL，处理默认头像逻辑"""
    if avatar_filename and avatar_filename != 'default_avatar.png':
        # 如果不是默认头像，添加上传路径
        return f"/static/uploads/avatars/{avatar_filename}"
    else:
        # 如果是默认头像或为空，使用默认头像路径
        return "/static/uploads/avatars/default_avatar.png"


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


@app.route('/post_detail/<int:post_id>')
def post_detail(post_id):
    """帖子详情页面"""
    post = Post.query.get_or_404(post_id)

    # 获取评论并按时间排序
    comments = Comment.query.filter_by(
        post_id=post_id).order_by(Comment.timestamp.asc()).all()

    # 创建评论表单
    form = CommentForm()

    # 获取相关帖子（同作者的其他帖子，最多5个）
    related_posts = Post.query.filter(
        Post.author_id == post.author_id,
        Post.id != post_id  # 排除当前帖子
    ).order_by(Post.timestamp.desc()).limit(5).all()

    return render_template('post_detail.html',
                           post=post,
                           comments=comments,
                           form=form,
                           related_posts=related_posts)


@app.route('/add_comment/<int:post_id>', methods=['POST'])
@login_required
def add_comment(post_id):
    """添加评论"""
    post = Post.query.get_or_404(post_id)
    form = CommentForm()

    if form.validate_on_submit():
        comment = Comment(
            content=form.content.data,
            author=current_user,
            post_id=post_id
        )
        db.session.add(comment)
        # 更新帖子评论计数
        post.comments_count = Comment.query.filter_by(post_id=post_id).count()
        db.session.commit()
        flash('评论已发布', 'success')
    else:
        for error in form.errors.values():
            flash(','.join(error), 'danger')

    return redirect(url_for('post_detail', post_id=post_id))


@app.route('/news')
def news():
    """新闻页面"""
    # 获取最新的新闻，按时间倒序排列
    news_items = News.query.order_by(News.timestamp.desc()).all()
    return render_template('news.html', news_items=news_items)


@app.route('/videos')
def videos():
    """视频页面"""
    # 获取最新的视频，按时间倒序排列
    videos = Video.query.order_by(Video.timestamp.desc()).all()
    return render_template('videos.html', videos=videos)


@app.route('/trending')
def trending():
    """热度排行页面"""
    from utils import calculate_daily_trends
    daily_trends = calculate_daily_trends()
    return render_template('trending.html', daily_trends=daily_trends)


@app.route('/forum')
def forum():
    """论坛页面"""
    # 获取最新的帖子，按时间倒序排列
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    # 创建发布帖子的表单
    form = PostForm() if current_user.is_authenticated else None
    return render_template('forum.html', posts=posts, form=form)


@app.route('/search')
def search():
    """搜索功能"""
    query = request.args.get('q', '')
    if query:
        # 搜索用户
        users = User.query.filter(User.username.contains(query)).all()
        # 搜索帖子
        posts = Post.query.filter(Post.title.contains(
            query) | Post.content.contains(query)).all()
        # 搜索视频
        videos = Video.query.filter(Video.title.contains(
            query) | Video.description.contains(query)).all()

        # 组合搜索结果
        results = []
        for user in users:
            results.append({'type': 'user', 'data': user,
                           'display_name': user.username})
        for post in posts:
            results.append({'type': 'post', 'data': post,
                           'display_name': post.title})
        for video in videos:
            results.append({'type': 'video', 'data': video,
                           'display_name': video.title})
    else:
        results = []

    return render_template('search_results.html', results=results, query=query)


@app.route('/profile/<username>')
def profile(username):
    """用户个人资料页面"""
    user = User.query.filter_by(username=username).first_or_404()

    # 获取用户发布的帖子
    user_posts = Post.query.filter_by(
        author_id=user.id).order_by(Post.timestamp.desc()).all()

    # 获取用户上传的视频
    user_videos = Video.query.filter_by(
        uploader_id=user.id).order_by(Video.timestamp.desc()).all()

    # 检查当前用户是否关注了该用户
    is_following = False
    if current_user.is_authenticated:
        is_following = current_user.is_following(user)

    return render_template('profile.html',
                           user=user,
                           posts=user_posts,
                           videos=user_videos,
                           is_following=is_following)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """编辑个人资料页面"""
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.bio = form.bio.data
        current_user.location = form.location.data
        current_user.website = form.website.data

        # 处理头像上传
        if form.avatar.data:
            avatar_file = form.avatar.data
            avatar_filename = save_image(avatar_file, os.path.join(
                UPLOAD_FOLDER, 'avatars'), size=(150, 150))
            current_user.avatar = avatar_filename

        db.session.commit()
        flash('个人资料已更新', 'success')
        return redirect(url_for('profile', username=current_user.username))

    return render_template('edit_profile.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """用户登录页面"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        flash('用户名或密码错误', 'danger')

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """用户注册页面"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('注册成功，请登录', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    """用户登出"""
    logout_user()
    return redirect(url_for('index'))


@app.route('/messages')
@login_required
def messages():
    """消息中心页面"""
    # 获取收到的消息
    received_messages = current_user.received_messages.order_by(
        Message.timestamp.desc()).all()
    # 获取发送的消息
    sent_messages = current_user.sent_messages.order_by(
        Message.timestamp.desc()).all()

    # 合并并按时间排序
    all_messages = sorted(received_messages + sent_messages,
                          key=lambda x: x.timestamp, reverse=True)

    # 获取最近联系人
    recent_contacts = []
    processed_usernames = set()
    for msg in all_messages:
        partner = msg.sender if msg.recipient_id == current_user.id else msg.recipient
        if partner.username not in processed_usernames:
            recent_contacts.append(partner)
            processed_usernames.add(partner.username)
            if len(recent_contacts) >= 10:  # 限制为最近10个联系人
                break

    return render_template('messages.html',
                           all_messages=all_messages,
                           recent_contacts=recent_contacts)


@app.route('/chat/<recipient>')
@login_required
def chat_window(recipient):
    """聊天窗口页面"""
    recipient_user = User.query.filter_by(username=recipient).first_or_404()

    # 获取与该用户的聊天记录
    chat_messages = Message.query.filter(
        ((Message.sender_id == current_user.id) & (Message.recipient_id == recipient_user.id)) |
        ((Message.sender_id == recipient_user.id) &
         (Message.recipient_id == current_user.id))
    ).order_by(Message.timestamp.asc()).all()

    form = MessageForm()
    return render_template('chat.html',
                           recipient=recipient_user,
                           chat_messages=chat_messages,
                           form=form)


@app.route('/admin')
@login_required
def admin():
    """管理员页面"""
    if not current_user.is_admin:
        flash('您没有权限访问此页面', 'danger')
        return redirect(url_for('index'))

    # 获取所有用户
    users = User.query.all()

    # 创建封禁用户表单
    ban_form = AdminUserBanForm()

    return render_template('admin/index.html', users=users, ban_form=ban_form)


@app.route('/follow/<username>')
@login_required
def follow(username):
    """关注用户"""
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('用户不存在', 'error')
        return redirect(url_for('index'))

    if user == current_user:
        flash('您不能关注自己', 'error')
        return redirect(url_for('profile', username=username))

    current_user.follow(user)
    db.session.commit()
    flash(f'您现在已关注 {username}', 'success')

    return redirect(url_for('profile', username=username))


@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    """取消关注用户"""
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('用户不存在', 'error')
        return redirect(url_for('index'))

    if user == current_user:
        flash('您不能取消关注自己', 'error')
        return redirect(url_for('profile', username=username))

    current_user.unfollow(user)
    db.session.commit()
    flash(f'您已取消关注 {username}', 'success')

    return redirect(url_for('profile', username=username))


@app.route('/user/<username>/following')
def show_following(username):
    """显示用户关注列表"""
    user = User.query.filter_by(username=username).first_or_404()
    following = user.followed.all()
    return render_template('user_list.html', users=following, title=f'{username} 关注的人')


@app.route('/user/<username>/followers')
def show_followers(username):
    """显示用户粉丝列表"""
    user = User.query.filter_by(username=username).first_or_404()
    followers = user.followers.all()
    return render_template('user_list.html', users=followers, title=f'{username} 的粉丝')


@app.route('/like_post/<int:post_id>', methods=['POST'])
@login_required
def like_post(post_id):
    """点赞帖子"""
    post = Post.query.get_or_404(post_id)

    # 检查用户是否已点赞
    existing_like = PostLike.query.filter_by(
        user_id=current_user.id, post_id=post_id).first()

    if existing_like:
        # 如果已点赞，则取消点赞
        db.session.delete(existing_like)
        post.likes_count = max(0, post.likes_count - 1)  # 确保不会变成负数
        liked = False
    else:
        # 如果未点赞，则添加点赞
        like = PostLike(user_id=current_user.id, post_id=post_id)
        db.session.add(like)
        post.likes_count += 1
        liked = True

    db.session.commit()

    return jsonify({'liked': liked, 'likes_count': post.likes_count})


@app.route('/like_video/<int:video_id>', methods=['POST'])
@login_required
def like_video(video_id):
    """点赞视频"""
    video = Video.query.get_or_404(video_id)

    # 检查用户是否已点赞
    existing_like = VideoLike.query.filter_by(
        user_id=current_user.id, video_id=video_id).first()

    if existing_like:
        # 如果已点赞，则取消点赞
        db.session.delete(existing_like)
        video.likes_count = max(0, video.likes_count - 1)  # 确保不会变成负数
        liked = False
    else:
        # 如果未点赞，则添加点赞
        like = VideoLike(user_id=current_user.id, video_id=video_id)
        db.session.add(like)
        video.likes_count += 1
        liked = True

    db.session.commit()

    return jsonify({'liked': liked, 'likes_count': video.likes_count})


@app.route('/like_news/<int:news_id>', methods=['POST'])
@login_required
def like_news(news_id):
    """点赞新闻"""
    news = News.query.get_or_404(news_id)

    # 检查用户是否已点赞
    existing_like = NewsLike.query.filter_by(
        user_id=current_user.id, news_id=news_id).first()

    if existing_like:
        # 如果已点赞，则取消点赞
        db.session.delete(existing_like)
        news.likes_count = max(0, news.likes_count - 1)  # 确保不会变成负数
        liked = False
    else:
        # 如果未点赞，则添加点赞
        like = NewsLike(user_id=current_user.id, news_id=news_id)
        db.session.add(like)
        news.likes_count += 1
        liked = True

    db.session.commit()

    return jsonify({'liked': liked, 'likes_count': news.likes_count})


@app.route('/like_<type>/<int:id>', methods=['POST'])
@login_required
def like_generic(type, id):
    """通用点赞接口，处理前端的动态请求"""
    if type == 'post':
        return like_post(id)
    elif type == 'video':
        return like_video(id)
    elif type == 'news':
        return like_news(id)
    else:
        return jsonify({'error': '不支持的类型'}), 400


@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    """编辑帖子"""
    post = Post.query.get_or_404(post_id)

    # 检查用户权限（必须是帖子作者或管理员）
    if post.author != current_user and not current_user.is_admin:
        flash('您没有权限编辑此帖子', 'danger')
        return redirect(url_for('post_detail', post_id=post_id))

    form = PostForm(obj=post)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data

        # 处理图片上传
        if form.image.data:
            image_file = form.image.data
            image_filename = save_image(image_file, os.path.join(
                UPLOAD_FOLDER, 'posts'), size=(800, 600))
            post.image_url = f'uploads/posts/{image_filename}'

        # 处理视频上传
        if form.video.data:
            video_file = form.video.data
            video_filename = save_file(
                video_file, os.path.join(UPLOAD_FOLDER, 'posts'))
            post.video_url = f'uploads/posts/{video_filename}'

        db.session.commit()
        flash('帖子已更新', 'success')
        return redirect(url_for('post_detail', post_id=post.id))

    return render_template('edit_post.html', form=form, post=post)


@app.route('/edit_video/<int:video_id>', methods=['GET', 'POST'])
@login_required
def edit_video(video_id):
    """编辑视频"""
    video = Video.query.get_or_404(video_id)

    # 检查用户权限（必须是视频上传者或管理员）
    if video.uploader != current_user and not current_user.is_admin:
        flash('您没有权限编辑此视频', 'danger')
        return redirect(url_for('video_detail', video_id=video_id))

    form = VideoForm(obj=video)
    if form.validate_on_submit():
        video.title = form.title.data
        video.description = form.description.data

        # 处理缩略图上传
        if form.thumbnail.data:
            thumbnail_file = form.thumbnail.data
            thumbnail_filename = save_image(thumbnail_file, os.path.join(
                UPLOAD_FOLDER, 'posts'), size=(400, 300))
            video.thumbnail_url = f'uploads/posts/{thumbnail_filename}'

        db.session.commit()
        flash('视频已更新', 'success')
        return redirect(url_for('video_detail', video_id=video.id))

    return render_template('edit_video.html', form=form, video=video)


@app.route('/news_detail/<int:news_id>')
def news_detail(news_id):
    """新闻详情页面"""
    news_item = News.query.get_or_404(news_id)

    # 增加浏览量
    news_item.views = news_item.views + 1 if news_item.views else 1
    db.session.commit()

    # 获取相关新闻（同一天发布的新闻，排除当前新闻）
    from sqlalchemy import extract
    related_news = News.query.filter(
        extract('year', News.timestamp) == extract(
            'year', news_item.timestamp),
        extract('month', News.timestamp) == extract(
            'month', news_item.timestamp),
        extract('day', News.timestamp) == extract('day', news_item.timestamp),
        News.id != news_id
    ).order_by(News.timestamp.desc()).limit(5).all()

    # 获取评论
    comments = Comment.query.filter_by(
        news_id=news_id).order_by(Comment.timestamp.asc()).all()

    # 创建评论表单
    form = CommentForm()

    return render_template('news_detail.html',
                           news=news_item,
                           related=related_news,
                           comments=comments,
                           comment_form=form)


@app.route('/video_detail/<int:video_id>')
@login_required
def video_detail(video_id):
    """视频详情页面"""
    video = Video.query.get_or_404(video_id)

    # 增加观看次数
    video.views = video.views + 1 if video.views else 1
    db.session.commit()

    # 获取相关视频（同一上传者的其他视频，最多5个）
    related_videos = Video.query.filter(
        Video.uploader_id == video.uploader_id,
        Video.id != video_id  # 排除当前视频
    ).order_by(Video.timestamp.desc()).limit(5).all()

    # 获取评论
    comments = Comment.query.filter_by(
        video_id=video_id).order_by(Comment.timestamp.asc()).all()

    # 创建评论表单
    form = CommentForm()

    return render_template('video_detail.html',
                           video=video,
                           related_videos=related_videos,
                           comments=comments,
                           form=form)


@app.route('/add_news_comment/<int:news_id>', methods=['POST'])
@login_required
def add_news_comment(news_id):
    """添加新闻评论"""
    news = News.query.get_or_404(news_id)
    form = CommentForm()

    if form.validate_on_submit():
        comment = Comment(
            content=form.content.data,
            author=current_user,
            news_id=news_id
        )
        db.session.add(comment)
        db.session.commit()
        flash('评论已发布', 'success')
    else:
        for error in form.errors.values():
            flash(','.join(error), 'danger')

    return redirect(url_for('news_detail', news_id=news_id))


@app.route('/add_comment_to_video/<int:video_id>', methods=['POST'])
@login_required
def add_comment_to_video(video_id):
    """添加视频评论"""
    video = Video.query.get_or_404(video_id)
    form = CommentForm()

    if form.validate_on_submit():
        comment = Comment(
            content=form.content.data,
            author=current_user,
            video_id=video_id
        )
        db.session.add(comment)
        db.session.commit()
        flash('评论已发布', 'success')
    else:
        for error in form.errors.values():
            flash(','.join(error), 'danger')

    return redirect(url_for('video_detail', video_id=video_id))


if __name__ == '__main__':
    app.run(debug=True)
