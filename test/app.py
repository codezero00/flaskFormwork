import os
import config
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)
ma = Marshmallow(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24))


class Reward(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reward_name = db.Column(db.String(125))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='rewards')  #


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User


class RewardSchema(ma.ModelSchema):
    class Meta:
        model = Reward


@app.route('/')
def index():
    one_user = User.query.all()
    user_schema = UserSchema(many=True)  # 用已继承ma.ModelSchema类的自定制类生成序列化类
    output = user_schema.dump(one_user)  # 生成可序列化对象
    return jsonify({'user': output})


#
if __name__ == '__main__':
    app.run()

# reference:https://juejin.im/post/5d3bc3d25188254cbc32b1cc
# https://www.youtube.com/watch?v=kRNXKzfYrPU

# 插入数据部分
# from app import db
# db.create_all()
# from app import User,Reward
# one = User(name='User One')
# two = User(name='User Two')
# db.session.add_all([one,two])
# db.session.commit()
#
# first = Reward(reward_name='Reward 1',user=one)
# second = Reward(reward_name='Reward 2',user=one)
# third = Reward(reward_name='Reward 3',user=two)
# db.session.commit()
