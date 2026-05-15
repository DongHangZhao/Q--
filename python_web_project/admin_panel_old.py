'''
Author: your name
Date: 2026-04-10 16:42:03
LastEditTime: 2026-04-10 16:42:03
LastEditors: your name
Description: In User Settings Edit
FilePath: /python_web_project/admin_panel.py
'''
"""
数据库可视化管理后台
使用 Flask-Admin 实现数据库的可视化查看、编辑、删除功能
"""

import os
import io
import csv
from flask_admin import Admin, expose, BaseView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for, flash, Response, send_file
from models import User, Post, Video, Comment, Message, News, NewsLike, PostLike, VideoLike, Trending, Follows, UserStatus, NewsOperationLog


class AdminModelView(ModelView):
    """自定义管理视图 - 需要管理员权限"""

    def is_accessible(self):
        """检查访问权限 - 只有管理员可以访问"""
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        """无权限时的回调"""
        return redirect(url_for('login'))

    # 列表显示配置
    page_size = 20
    can_view_details = True
    can_export = True
    export_types = ['csv', 'xlsx']

    # 中文化列名映射
    column_chinese_names = {}

    # 使用自定义模板
    list_template = 'admin/model_list.html'

    @expose('/export/csv/')
    def export_csv(self):
        """导出CSV文件，支持UTF-8 BOM编码"""
        from flask import request
        return_url = request.args.get('url', None)

        # 获取查询结果
        query = self.get_query()
        data = query.all()

        # 获取列名
        column_names = self.column_list
        # 使用中文化列名
        chinese_names = getattr(self, 'column_chinese_names', {})
        headers = [chinese_names.get(col, col) for col in column_names]

        # 创建UTF-8 BOM编码的CSV
        output = io.StringIO()
        output.write('\ufeff')  # UTF-8 BOM
        writer = csv.writer(output)
        writer.writerow(headers)

        for item in data:
            row = []
            for col in column_names:
                value = getattr(item, col, '')
                # 处理关联对象
                if callable(value):
                    value = ''
                elif hasattr(value, 'username'):  # 关联用户对象
                    value = value.username
                elif value is None:
                    value = ''
                row.append(str(value))
            writer.writerow(row)

        output.seek(0)

        # 创建响应
        return Response(
            output.getvalue().encode('utf-8-sig'),
            mimetype='text/csv; charset=utf-8-sig',
            headers={
                'Content-Disposition': f'attachment; filename*=UTF-8\'\'{self.name}.csv'
            }
        )


def init_admin(app, db):
    """初始化管理后台"""
    # 为Flask-Admin创建独立的模板目录
    import os
    admin_template_path = os.path.join(
        os.path.dirname(__file__), 'templates', 'flask_admin')
    os.makedirs(admin_template_path, exist_ok=True)

    admin = Admin(
        app,
        name='咫尺天涯数据库管理',
        url='/dbadmin'
    )

    # 注册所有模型的管理视图
    admin.add_view(UserAdminView(User, db.session, name='用户管理', category='用户'))
    admin.add_view(PostAdminView(Post, db.session, name='动态管理', category='内容'))
    admin.add_view(NewsAdminView(News, db.session, name='新闻管理', category='内容'))
    admin.add_view(CommentAdminView(
        Comment, db.session, name='评论管理', category='内容'))
    admin.add_view(ModelView(Message, db.session, name='私信管理', category='内容'))
    admin.add_view(ModelView(NewsLike, db.session, name='新闻点赞', category='互动'))
    admin.add_view(ModelView(PostLike, db.session, name='动态点赞', category='互动'))
    admin.add_view(ModelView(VideoLike, db.session,
                   name='视频点赞', category='互动'))
    admin.add_view(ModelView(Trending, db.session, name='热度排行', category='系统'))
    admin.add_view(ModelView(Follows, db.session, name='关注关系', category='用户'))
    admin.add_view(ModelView(UserStatus, db.session,
                   name='用户状态', category='用户'))
    admin.add_view(ModelView(NewsOperationLog, db.session,
                   name='操作日志', category='系统'))

    return admin


# ==================== 视图类定义 ====================

class UserAdminView(AdminModelView):
    """用户管理视图"""
    column_list = ('id', 'username', 'email', 'is_admin', 'bio')
    column_searchable_list = ('username', 'email')
    column_filters = ('is_admin',)
    column_editable_list = ('is_admin', 'email')
    form_columns = ('username', 'email', 'is_admin', 'bio')

    # 中文化列名
    column_chinese_names = {
        'id': 'ID',
        'username': '用户名',
        'email': '邮箱',
        'is_admin': '管理员',
        'bio': '个人简介'
    }

    # 中文化列标签
    column_labels = column_chinese_names


class PostAdminView(AdminModelView):
    """动态管理视图"""
    column_list = ('id', 'title', 'author', 'timestamp',
                   'views', 'likes_count', 'comments_count')
    column_searchable_list = ('title', 'content')
    form_columns = ('title', 'content', 'author')

    column_chinese_names = {
        'id': 'ID',
        'title': '标题',
        'author': '作者',
        'timestamp': '发布时间',
        'views': '浏览数',
        'likes_count': '点赞数',
        'comments_count': '评论数'
    }
    column_labels = column_chinese_names


class NewsAdminView(AdminModelView):
    """新闻管理视图"""
    column_list = ('id', 'title', 'source', 'timestamp',
                   'views', 'likes_count', 'comments_count')
    column_searchable_list = ('title', 'content', 'summary')
    column_filters = ('source',)
    form_columns = ('title', 'content', 'summary', 'source', 'image_url')

    column_chinese_names = {
        'id': 'ID',
        'title': '标题',
        'source': '来源',
        'timestamp': '发布时间',
        'views': '浏览数',
        'likes_count': '点赞数',
        'comments_count': '评论数'
    }
    column_labels = column_chinese_names


class CommentAdminView(AdminModelView):
    """评论管理视图"""
    column_list = ('id', 'author', 'content', 'timestamp')
    column_searchable_list = ('content',)
    form_columns = ('content', 'author')

    column_chinese_names = {
        'id': 'ID',
        'author': '作者',
        'content': '内容',
        'timestamp': '时间'
    }
    column_labels = column_chinese_names
