"""
DAO层 和 service 层合并
数据库操作层 和 服务层

1. 例子
class todo1DAO(object):
    def __init__(self):
        self.counter = 0
        self.todo1s = []

    def get(self, id):
        for todo1 in self.todo1s:
            if todo1['id'] == id:
                return todo1
        api.abort(404, "todo1 {} doesn't exist".format(id))

    def create(self, data):
        todo1 = data
        todo1['id'] = self.counter = self.counter + 1
        self.todo1s.append(todo1)
        return todo1

    def update(self, id, data):
        todo1 = self.get(id)
        todo1.update(data)
        return todo1

    def delete(self, id):
        todo1 = self.get(id)
        self.todo1s.remove(todo1)
"""

from .model import session
from .model import scapp, ScappSchema
from sqlalchemy import text

class AppService(object):
    """
    sc_app表相关操作
    """

    def __init__(self):
        self.__MODEL = scapp  # 将scapp model 赋值给 __MODEL 减少代码改动量
        self.__SCHEMA = ScappSchema  # ScappSchema Schema 赋值给 __SCHEMA 减少代码改动量

    def get(self, id: str) -> dict:
        """
        查询详情 【单个查询】
        :param id:
        :return:
        """
        # 实例化ScappSchema 用已继承ma.ModelSchema类的自定制类生成序列化类 many=True 可以反序列化多条 many=False 只能反序列化一条
        one_res = session.query(self.__MODEL).filter(self.__MODEL.id == id).all()
        # 棉花糖 反序列化
        schema = self.__SCHEMA(many=True)
        output = schema.dump(one_res)  # 生成可序列化对象
        return output

    def getList(self, data: dict) -> list:
        """
        查询列表 【多个查询】
        :param data: { CurrentPage PageSize Where OrderBy}
        :return:
        """
        print(data)
        # 实例化ScappSchema 用已继承ma.ModelSchema类的自定制类生成序列化类 many=True 可以反序列化多条 many=False 只能反序列化一条
        one_res = session.query(self.__MODEL).filter(text("1=:p1")).params({'p1': 2}).order_by(text('id desc')).limit(10).offset(0).all()
        # 棉花糖 反序列化
        schema = self.__SCHEMA(many=True)
        output = schema.dump(one_res)  # 生成可序列化对象
        return output

    def create(self, data):
        newRecord = self.__MODEL(id=data['id'], app_name=data['app_name'])
        session.add(newRecord)
        session.commit()
        # 棉花糖反序列化
        schema = self.__SCHEMA(many=False)
        output = schema.dump(newRecord)  # 生成可序列化对象
        return output

    def update(self, id, data):
        pass

    @staticmethod
    def delete(self, id):
        pass
