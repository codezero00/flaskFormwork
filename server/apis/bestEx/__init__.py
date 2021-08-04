"""
最佳例子
"""
from flask_restx import Api

from .view import ns

api = Api(title="bestEx API", version="1.0", description="A simple bestEx API",)

api.add_namespace(ns)
