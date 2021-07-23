from flask_restx import Api

from .auth import api as auth_api

api = Api(title="auth API", version="1.0", description="A simple demo API",)

api.add_namespace(auth_api)
