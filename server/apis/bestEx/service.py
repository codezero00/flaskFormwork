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
from server.utils import Page, next_id


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

    def getPageList(self, data: dict) -> dict:
        """
        查询列表 【分页查询】
        :param data: { CurrentPage PageSize Where OrderBy}
        :return: dict(page=p.GetDict, res=list)
        """
        print(data)
        # num = session.query(self.__MODEL).filter(text("1=:p1")).params({'p1': 1}).order_by(text('id desc')).count()
        _text = data['Where'].get('text', '')  # 获取 where 字典 text值
        _params = data['Where'].get('params', '')  # 获取 where 字典 params值
        # 获取查询总条数值
        num = session.query(self.__MODEL).filter(text(_text)).params(_params).order_by(text('id desc')).count()
        p = Page(num, int(data['CurrentPage']), int(data['PageSize']))  # 构造page类
        if num == 0:

            return dict(page=p.GetDict, res=[])
        else:
            # 实例化ScappSchema 用已继承ma.ModelSchema类的自定制类生成序列化类 many=True 可以反序列化多条 many=False 只能反序列化一条
            one_res = session.query(self.__MODEL).filter(text(_text)).params(_params).order_by(text('id desc')).limit(
                p.limit).offset(p.offset).all()

            # 棉花糖 反序列化
            schema = self.__SCHEMA(many=True)
            output = schema.dump(one_res)  # 生成可序列化对象
            return dict(page=p.GetDict, res=output)

    def create(self, data):
        """
        插入一条数据
        :param data:
        :return:
        """
        data['id'] = next_id()
        # del data['createtime'], data['updatetime']  # 不能使用del 无key值时会报错
        data.pop('createtime', '')
        data.pop('updatetime', '')
        # newRecord = self.__MODEL(id=data['id'], app_name=data['app_name'])
        newRecord = self.__MODEL(**data)
        session.add(newRecord)
        session.commit()

        # 棉花糖反序列化
        schema = self.__SCHEMA(many=False)
        output = schema.dump(newRecord)  # 生成可序列化对象
        return output

    def update(self, id, data):
        """
        修改一条数据
        :param id:
        :param data:
        :return:
        """
        # del data['id'], data['createtime'], data['updatetime']  # 不能使用del 无key值时会报错
        data.pop('id', '')  # 删除id字段
        data.pop('createtime', '')
        data.pop('updatetime', '')
        print(data)
        # 根据Id查询需要更新的行
        session.query(self.__MODEL).filter(self.__MODEL.id == id).update(data)
        session.commit()

        return dict(id=id, data=data)

    def delete(self, id):
        """
        删除一条数据
        :param id:
        :return:
        """
        session.query(self.__MODEL).filter(self.__MODEL.id == id).delete()
        session.commit()

        return dict(id=id)
