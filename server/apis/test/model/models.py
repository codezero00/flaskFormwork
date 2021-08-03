"""
SQLAlchemy 模型
"""

from server import db, create_app
from sqlalchemy.ext.automap import automap_base

app = create_app()
# 将所有现有表反射为SQLAlchemy 类
with app.app_context():  # 获取上下文 使用 db.init_app(app) 加载sqlalchemy时，必须要这样写
    metadata = db.metadata
    engine = db.engine
    session = db.session

Base = automap_base(metadata=metadata) #从metadata中生成所有的映射关系为Base
Base.prepare(engine, reflect=True)

# 分割符号  【在先添加需要引入的表】
scapp = Base.classes.sc_app