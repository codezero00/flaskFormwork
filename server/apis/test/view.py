# server apis test view.py
import json
from flask import request, render_template, make_response, jsonify
from flask_restx import Namespace, Resource, fields
from .DAO import AppDAO
from server import AuthError

ns = Namespace('test', description='test Namespace', ordered=True)

# @ns.route("/url1/", strict_slashes=False)  # 实际访问地址 /api/test/
# class TestHandler(Resource):
#
#     def get(self):
#         # 如果使用模板的块，需要使用 make_response
#         # return make_response(render_template('index.html', data=res), 200)
#
#         # 使用 jsonify 是为了返回json数据的同时，相比于 json.dumps() 其会自动修改 content-type 为 application/json
#         # 另外，如果使用 jsonify()的同时，还想自定义返回状态码，可以使用 make_response(jsonify(data=data), 201)
#         return jsonify()
#
#     def post(self):
#         pass
#
#     def put(self):
#         pass
#
#     def delete(self):
#         pass

testmodel = ns.model('scapp', {
    'id': fields.String,
    'createuserid': fields.String,
    'createtime': fields.String,
    'updateuserid': fields.String,
    'updatetime': fields.String,
    'app_name': fields.String,
    'app_name_en': fields.String,
    'app_name_en_short': fields.String,
    'remark': fields.String,
    'content': fields.String,
    'link_url': fields.String,
    'code': fields.String,
    'icon': fields.String,
    'module': fields.String,
    'defaultregister': fields.String,
    'entry': fields.String,
    'routerbase': fields.String,
    'nomenu': fields.String
})

from .model import ScappSchema


@ns.route("/<string:id>", strict_slashes=False)  # 实际访问地址 /api/test/
@ns.param("id", "The scapp identifier")
class TestHandler2(Resource):

    @ns.doc(
        "Get a specific user",
        responses={
            200: ("User data successfully sent", testmodel),
            404: "User not found!",
        },
    )
    # @ns.marshal_with(testmodel, code=201)
    def get(self, id):
        try:
            res = AppDAO.get(id=id)
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


@ns.route("/", strict_slashes=False)  # 实际访问地址 /api/test/
class TestHandler2List(Resource):

    @ns.doc(
        "list specific scapp",
        responses={
            200: ("User data successfully sent", testmodel),
            404: "User not found!",
        },
    )
    def post(self):
        """ 获取匹配app """
        res = AppDAO.get(id='1')
        data = dict(code=200, message="", data=res)
        return jsonify(data)

    def get(self):
        """ get all scapp """
        pass