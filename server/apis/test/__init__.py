from flask_restx import Api

from .view import ns as test_ns

api = Api(title="test API", version="1.0", description="A simple test API",)

api.add_namespace(test_ns)
