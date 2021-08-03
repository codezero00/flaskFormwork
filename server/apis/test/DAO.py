"""
DAO层
数据库操作层

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

from .model import scapp, ScappSchema, session


class AppDAO(object):
    """
    sc_app表相关操作
    """

    def __init__(self):
        pass

    @staticmethod
    def get(id: str) -> dict:
        """
        查询详情 【单个查询】
        :param id:
        :return:
        """
        # 实例化ScappSchema 用已继承ma.ModelSchema类的自定制类生成序列化类 many=True 可以反序列化多条 many=False 只能反序列化一条
        app_schema = ScappSchema(many=True)
        one_res = session.query(scapp).filter(scapp.id == id).all()
        print(one_res)
        output = app_schema.dump(one_res)  # 生成可序列化对象
        print(output)
        return output

    def getList(self, data: dict) -> list:
        """
        查询列表 【多个查询】
        :param data:
        :return:
        """
        return []

    def create(self, data):
        pass

    def update(self, id, data):
        pass

    def delete(self, id):
        pass
