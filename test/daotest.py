"""
sqlalchemy反射已经存在的数据库表
"""
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.ext.automap import automap_base

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:zyjs2018!@172.16.4.110:3306/sc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
ma = Marshmallow(app)

# from sqlalchemy import create_engine, Table, MetaData
# from sqlalchemy.orm import Session

# engine = create_engine('mysql+mysqlconnector://root:zyjs2018!@172.16.4.110:3306/sc', echo=True)

# 反射数据库单表
# metadata = MetaData()
# Admin = Table('sc_app', metadata, autoload=True, autoload_with=db)
# session = Session(db)

'''反射数据库所有的表
Base = automap_base()
Base.prepare(engine, reflect=True)
Admin = Base.classes.sc_app
'''

# res = session.query(Admin).all()
# print(res.id, res)
# print(res)


# metadata = db.MetaData()


# Admin = db.Table('sc_app', metadata, autoload=True, autoload_with=db.engine)
# res = db.session.query(Admin).all()
# print(res)
# print(Admin)
# print(type(Admin))
#
# class AdminSchema(ma.SQLAlchemySchema):
#     class Meta:
#         model = Admin
#         load_instance = True

# admin_schema = AdminSchema(many=True)  # 用已继承ma.ModelSchema类的自定制类生成序列化类
# output = admin_schema.dump(res)  # 生成可序列化对象
#
# print(admin_schema)
# print(output)


# author = Admin(app_name="test")
# print(author)
# admin_schema = AdminSchema()
# dump_data = admin_schema.dump(author)
# print(dump_data)


# Base = automap_base(metadata=metadata) #从metadata中生成所有的映射关系为Base
# Base.prepare(db.engine, reflect=True)
# Admin2 = Base.classes.sc_app
# # De = Base.classes.tbDeployment #将表映射到类上
# print(Admin2)
# res2 = db.session.query(Admin2).all()
# print(res2)
#
# for result in db.session.query(Admin2).all():
#     print(result.app_name)


class sc_app(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    app_name = db.Column(db.String(50))





class ScappSchema(ma.SQLAlchemySchema):
    class Meta:
        model = sc_app




one_user = sc_app.query.all()
user_schema = ScappSchema(many=True) #用已继承ma.ModelSchema类的自定制类生成序列化类
print(one_user)
output = user_schema.dump(one_user) #生成可序列化对象
print(output)