# server  __init__.py
from flask import Flask, render_template, jsonify
from server.jwt import AuthError


def create_app():
    # 1.实例化 app 实例
    app = Flask(__name__)
    # 2.加载配置文件 从 根目录下找
    app.config.from_object('config')
    # 3.注册扩展模块
    register_extension(app)
    # 4.注册蓝图，视图函数
    register_blueprint(app)

    # 读取配置文件
    # app.config.from_pyfile(config_filename)

    @app.route('/')
    def home():
        return render_template("index.html")

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        """
        使用 errorhandler 装饰器进行异常处理
        将 raise AuthError() 产生的错误，使用jsonify
        :param ex:
        :return:
        """
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    return app


def register_extension(app):
    """
    加载扩展模块，并且配置各个模块
    :param app:
    :return:
    """
    # 加载扩展模块
    from server.extension import cors
    # from server.extension import jwt
    from server.extension import db
    # from extension import ma
    # from extension import migrate
    #  将扩展模块注册到app 中
    cors.init_app(app)
    db.init_app(app)
    # jwt.init_app(app)
    # ma.init_app(app)
    # migrate.init_app(app, db=db)


def register_blueprint(app):
    """
    注册蓝图
    :param app:
    :return:
    """
    # 注册根蓝图 父类蓝图 [ps.嵌套蓝图]
    from server.api import rootBP
    app.register_blueprint(rootBP)
