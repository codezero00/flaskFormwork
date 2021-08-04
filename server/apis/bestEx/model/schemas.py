"""
使用ma 棉花糖 进行反序列化
"""
from server import ma
from .models import scapp


# 使用 Marshmallow 反序列化 SQLAlchemy
# !!!!!! 注意   这里使用SQLAlchemyAutoSchema
class ScappSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = scapp
        include_fk = True
