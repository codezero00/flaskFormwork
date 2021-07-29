import os

"""
设置环境变量 
带'__' 开头的为自定义环境变量 
不带'__' 开头的为系统使用环境变量
os.environ.get(key, default)
"""
# 系统
SWAGGER_UI_DOC_EXPANSION = 'none'  # 指定 swagger 初始展开状态
SECRET_KEY = 'asdfasdf'
DEBUG = True

AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN", default='http://172.16.4.106:8080/auth/realms/master')
API_IDENTIFIER = os.environ.get("API_IDENTIFIER", default='')
ALGORITHMS = ["RS256"]
API_AUDIENCE = os.environ.get("API_IDENTIFIER", default='master-realm')

# 自定义
SQLALCHEMY_DATABASE_URI = 'sqlite://test.db'
__HOST = os.environ.get('HOST', default='172.16.4.110')
__DATABASE = os.environ.get('DATABASE', default='sc')
__USER = os.environ.get('USER', default='root')
__PASSWORD = os.environ.get('PASSWORD', default='zyjs2018!')
