# server apis test view.py
from flask import jsonify, request, Response
from flask_restx import Namespace, Resource
from flask_accepts import accepts, responds
from server import AuthError
from .service import AppService
from .model import ScappSchema
from server.jwt import requires_auth  # openid认证装饰器

ns = Namespace('best', description='最佳实践示例', ordered=True)


@ns.route("/<string:id>")  # 实际访问地址 /api/test/
@ns.param("id", "sc_app表的主键")
class TestHandler(Resource):
    """
    查询详情、更新、删除
    """

    @responds(schema=ScappSchema)
    def get(self, id: str) -> Response:
        """
        根据ID获取1条记录
        :param id:
        :return:
        """
        try:
            _service = AppService()
            res = _service.get(id=id)
            data = dict(code=200, message="", data=res)
            return jsonify(data)
        except Exception as e:
            raise AuthError({"code": 500,
                             "message": str(e),
                             "data": ""}, 500)

    @accepts(schema=ScappSchema, api=ns)  # parsed_obj
    @requires_auth # 接口需要jwt登陆认证
    def put(self, id: str) -> Response:
        """
        根据ID更新记录
        Update a given resource
        :param id:
        :return:
        """
        try:
            args = request.parsed_obj
            _service = AppService()
            res = _service.update(id=id, data=args)
            data = dict(code=200, message="update sucess", data=res)
            return jsonify(data)
        except Exception as e:
            raise AuthError({"code": 500,
                             "message": str(e),
                             "data": ""}, 500)

    @requires_auth   # 接口需要jwt登陆认证
    def delete(self, id: str) -> Response:
        """
        根据ID删除1条记录
        :param id:
        :return:
        """
        try:
            _service = AppService()
            res = _service.delete(id=id)
            data = dict(code=200, message="delete sucess", data=res)
            return jsonify(data)
        except Exception as e:
            raise AuthError({"code": 500,
                             "message": str(e),
                             "data": ""}, 500)


@ns.route("/")  # 实际访问地址 /api/test/
class TestHandlerList(Resource):
    """
    分页查询、创建记录
    """

    @accepts(schema=ScappSchema, api=ns)  # parsed_obj
    @responds(schema=ScappSchema)
    def post(self):
        """ 创建1条记录 """
        try:
            args = request.parsed_obj
            _service = AppService()
            res = _service.create(data=args)
            data = dict(code=200, message="create sucess", data=res)
            return jsonify(data)
        except Exception as e:
            raise AuthError({"code": 500,
                             "message": str(e),
                             "data": ""}, 500)

    @accepts(
        dict(name="CurrentPage", type=int, required=True, default=1),  # parsed_args
        dict(name="PageSize", type=int, required=True, default=10),  # parsed_args
        dict(name="Where", type=str, help="""{ "text": "id>:p1 and cl2=:p2" , \n "params": { "p1": 1,"p2": 2 }}""",
             default="""{ "text": "" , "params": "" }"""),
        dict(name="OrderBy", type=str, help="""id desc""", default='id desc'),
        api=ns,
    )
    @responds(schema=ScappSchema, many=True)
    # @requires_auth
    def get(self) -> Response:
        """
        page查询
        List all todos
        :return:
        """
        try:
            args = request.parsed_args
            # 缺失值处理
            args = dict(CurrentPage=args.get('CurrentPage', 1),
                        PageSize=args.get('PageSize', 10),
                        Where=eval(args.get('Where', """ {"text": "", "params": ""} """)),
                        OrderBy=args.get('OrderBy', 'id desc'))
            _service = AppService()
            res = _service.getPageList(data=args)
            data = dict(code=200, message="", data=res)
            return jsonify(data)
        except Exception as e:
            raise AuthError({"code": 500,
                             "message": str(e),
                             "data": ""}, 500)
