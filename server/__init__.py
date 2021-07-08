# server  __init__.py
from flask import Flask, render_template

def create_app(config_filename):
    # 创建Flask对象
    app = Flask(__name__)
    app.config.SWAGGER_UI_DOC_EXPANSION = 'none'  # 指定 swagger 初始扩展状态
    # 读取配置文件
    # app.config.from_pyfile(config_filename)
    # 注册根蓝图 父类蓝图 [ps.嵌套蓝图]
    from server.api import rootBP
    app.register_blueprint(rootBP)

    @app.route('/')
    def home():
        return render_template("index.html")

    return app
