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
# class AdminSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Admin
#         load_instance = True
#
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

# 例子 2
# 将所有现有表反射为SQLAlchemy 类
# metadata = db.MetaData()
Base = automap_base(metadata=db.metadata) #从metadata中生成所有的映射关系为Base
Base.prepare(db.engine, reflect=True)
Admin2 = Base.classes.sc_app
# De = Base.classes.tbDeployment #将表映射到类上
# print(Admin2)
# print(type(Admin2))
# res2 = db.session.query(Admin2).all()
# print(res2)

# for result in db.session.query(Admin2).all():
#     print(result.app_name)

# 使用 Marshmallow 反序列化 SQLAlchemy
# !!!!!! 注意   这里使用SQLAlchemyAutoSchema
class ScappSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Admin2
        include_fk = True


one_user = db.session.query(Admin2).all()
user_schema = ScappSchema(many=True)  # 用已继承ma.ModelSchema类的自定制类生成序列化类
print(one_user)
output = user_schema.dump(one_user)  # 生成可序列化对象
print(output)



# 例子 3

# class sc_app(db.Model):
#     id = db.Column(db.String(50), primary_key=True)
#     app_name = db.Column(db.String(50))
#
#
# # !!!!!! 注意   这里使用SQLAlchemyAutoSchema
# class ScappSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = sc_app
#         include_fk = True
#
#
# one_user = sc_app.query.all()
# user_schema = ScappSchema(many=True)  # 用已继承ma.ModelSchema类的自定制类生成序列化类
# print(one_user)
# output = user_schema.dump(one_user)  # 生成可序列化对象
# print(output)


# 例子 4

# class Author(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255))
#
#
# class Book(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(255))
#     author_id = db.Column(db.Integer, db.ForeignKey("author.id"))
#     author = db.relationship("Author", backref="books")
#
#
# class AuthorSchema(ma.SQLAlchemySchema):
#     class Meta:
#         model = Author
#
#     id = ma.auto_field()
#     name = ma.auto_field()
#     books = ma.auto_field()
#
#
# class BookSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Book
#         include_fk = True
#
#
# db.create_all()  # 在数据库创建表
# author_schema = AuthorSchema()
# book_schema = BookSchema()
# author = Author(name="Chuck Paluhniuk")
# book = Book(title="Fight Club", author=author)
# db.session.add(author)
# db.session.add(book)
# db.session.commit()
# out = author_schema.dump(author)
# # {'id': 1, 'name': 'Chuck Paluhniuk', 'books': [1]}
# print(out)