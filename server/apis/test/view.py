# server apis test view.py
from flask import jsonify, request
from flask_restx import Namespace, Resource, fields
from .service import AppService
from server import AuthError

ns = Namespace('test', description='test Namespace', ordered=True)

# testmodel = ns.model('scapp', {
#     'id': fields.String,
#     'createuserid': fields.String,
#     'createtime': fields.String,
#     'updateuserid': fields.String,
#     'updatetime': fields.String,
#     'app_name': fields.String,
#     'app_name_en': fields.String,
#     'app_name_en_short': fields.String,
#     'remark': fields.String,
#     'content': fields.String,
#     'link_url': fields.String,
#     'code': fields.String,
#     'icon': fields.String,
#     'module': fields.String,
#     'defaultregister': fields.String,
#     'entry': fields.String,
#     'routerbase': fields.String,
#     'nomenu': fields.String
# })

@ns.route("/<string:id>", strict_slashes=False)  # 实际访问地址 /api/test/
@ns.param("id", "The scapp identifier")
class TestHandler2(Resource):

    # @ns.doc(
    #     "Get a specific user",
    #     responses={
    #         200: ("User data successfully sent", testmodel),
    #         404: "User not found!",
    #     },
    # )
    # @ns.marshal_with(testmodel, code=201)
    def get(self, id):
        try:
            res = AppService.get(id=id)
            data = dict(code=200, message="", data=res)
            return jsonify(data)
        except Exception as e:
            raise AuthError({"code": 500,
                             "message": str(e),
                             "data": ""}, 500)

    def put(self, id):
        pass

    def delete(self, id):
        pass

from flask_accepts import accepts, responds
from .model import ScappSchema

@ns.route("/", strict_slashes=False)  # 实际访问地址 /api/test/
class TestHandler2List(Resource):

    # @ns.doc(
    #     "list specific scapp",
    #     parser=parser,
    #     responses={
    #         200: ("User data successfully sent", testmodel),
    #         404: "User not found!",
    #     },
    # )
    @accepts(
        dict(name="hey", type=str),  # parsed_args
        dict(name="test", type=int, required=True, default=3),  # parsed_args
        schema=ScappSchema,  # parsed_obj
        api=ns,
    )
    @responds(schema=ScappSchema)
    def post(self):
        """ 获取匹配app """
        args = request.parsed_obj
        print(request.parsed_obj)
        print(request.parsed_args)
        res = AppService.get(id=1)
        data = dict(code=200, message="", data=res)
        return jsonify(data)

    @accepts(schema=ScappSchema, api=ns)
    @responds(schema=ScappSchema)
    def put(self):
        """ get all scapp """
        print(request.parsed_obj)
        print(request.parsed_args)
        return 1
