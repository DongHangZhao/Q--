"""
项目配置文件
定义应用程序的各种配置参数
"""

import os

class Config:
    """基础配置类"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-for-python-web-project'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.dirname(__file__), 'app.db')  # 修复数据库路径
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 添加配置来处理日期时间格式
    SQLALCHEMY_ENGINE_OPTIONS = {
        'connect_args': {
            'check_same_thread': False,  # SQLite特殊配置
            'detect_types': 3  # 启用类型检测
        }
    }
    
    # 应用程序特定配置
    APP_NAME = '咫尺天涯 - 社交平台'
    VERSION = '1.0.0'
    AUTHOR = '赵栋行'
    
    # 文件上传配置
    MAX_CONTENT_LENGTH = 1024 * 1024 * 1024  # 1GB max file size
    UPLOAD_FOLDER = 'static/uploads'
    
    # 分页配置
    ITEMS_PER_PAGE = 10

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# 配置字典
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}