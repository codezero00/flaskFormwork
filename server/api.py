# server api.py
import os
from flask import Blueprint
from flask_restx import Api

# from server.apis.test.view import ns as test_ns

# 定义项目名称 环境变量
PROJECT_NAME = os.environ.get("PROJECT_NAME", "defaultApp")
# 定义版本 环境变量
VERSION = os.environ.get("VERSION", "v1")

# 定义根蓝图 名称为项目名称环境变量
rootBP = Blueprint(f'{PROJECT_NAME}', __name__, url_prefix=f'/{PROJECT_NAME}/')

# 定义子蓝图
# 注册
testBP = Blueprint('test', __name__, url_prefix=f'/apis/test/{VERSION}')
rootBP.register_blueprint(testBP)  # 将test子蓝图注册到根蓝图

zooBP = Blueprint('zoo', __name__, url_prefix=f'/apis/zoo/{VERSION}')
rootBP.register_blueprint(zooBP)  # 将zoo子蓝图注册到根蓝图

authBP = Blueprint('auth', __name__, url_prefix=f'/apis/auth/{VERSION}')
rootBP.register_blueprint(authBP)  # 将zoo子蓝图注册到根蓝图

# api 注册到 testBP 蓝图
from server.apis.test import api as testapi

testapi.init_app(testBP)

# api 注册到 zooBP 蓝图
from server.apis.zoo import api as zooapi

zooapi.init_app(zooBP)

# api 注册到 zooBP 蓝图
from server.apis.auth import api as authapi

authapi.init_app(authBP)

# 自定义swagger ui
# @api.documentation
# def custom_ui():
#     """
#     这里是使用 templates 和 static 里面的文件进行的新 swagger ui 文件
#     :return:
#     """
#     return render_template("swagger-ui.html", title=api.title, specs_url=api.specs_url)
