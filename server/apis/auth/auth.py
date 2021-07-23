from flask_restx import Namespace, Resource, fields
from flask import jsonify

api = Namespace("auth", description="auth related operations keycloak 权限认证")

@api.route("/url1/", strict_slashes=False)  # 实际访问地址 /api/test/
class TestHandler(Resource):

    def get(self):
        # 如果使用模板的块，需要使用 make_response
        # return make_response(render_template('index.html', data=res), 200)

        # 使用 jsonify 是为了返回json数据的同时，相比于 json.dumps() 其会自动修改 content-type 为 application/json
        # 另外，如果使用 jsonify()的同时，还想自定义返回状态码，可以使用 make_response(jsonify(data=data), 201)
        return jsonify(dict(haha='1234', tk='token'))

    def post(self):
        return jsonify(dict(haha='post'))

    def put(self):
        pass

    def delete(self):
        pass