import json
from urllib.request import urlopen
from functools import wraps

from flask import request, _request_ctx_stack
from jose import jwt

from config import AUTH0_DOMAIN, ALGORITHMS, API_AUDIENCE


# Error handler
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# @APP.errorhandler(AuthError)
# def handle_auth_error(ex):
#     response = jsonify(ex.error)
#     response.status_code = ex.status_code
#     return response

def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                         "description":
                             "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                         "description":
                             "Authorization header must start with"
                             " Bearer"}, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                         "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                         "description":
                             "Authorization header must be"
                             " Bearer token"}, 401)

    token = parts[1]
    return token


def requires_auth(f):
    """Determines if the Access Token is valid
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        jsonurl = urlopen(AUTH0_DOMAIN + "/protocol/openid-connect/certs")
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer=AUTH0_DOMAIN
                )
            except jwt.ExpiredSignatureError:
                raise AuthError({"code": "token_expired",
                                 "description": "token is expired"}, 401)
            except jwt.JWTClaimsError:
                raise AuthError({"code": "invalid_claims",
                                 "description":
                                     "incorrect claims,"
                                     "please check the audience and issuer"}, 401)
            except Exception:
                raise AuthError({"code": "invalid_header",
                                 "description":
                                     "Unable to parse authentication"
                                     " token."}, 401)

            _request_ctx_stack.top.current_user = payload
            return f(*args, **kwargs)
        raise AuthError({"code": "invalid_header",
                         "description": "Unable to find appropriate key"}, 401)

    return decorated




# def get_token_auth_header_1(__request):
#     """
#     获取request header 里面的 token字符串
#     :param request:
#     :return:
#     """
#     auth = __request.headers.get("Authorization", None)
#     if not auth:
#         raise AuthError({"code": "authorization_header_missing",
#                          "description":
#                              "Authorization header is expected"}, 401)
#
#     parts = auth.split()
#
#     if parts[0].lower() != "bearer":
#         raise AuthError({"code": "invalid_header",
#                          "description":
#                              "Authorization header must start with"
#                              " Bearer"}, 401)
#     elif len(parts) == 1:
#         raise AuthError({"code": "invalid_header",
#                          "description": "Token not found"}, 401)
#     elif len(parts) > 2:
#         raise AuthError({"code": "invalid_header",
#                          "description":
#                              "Authorization header must be"
#                              " Bearer token"}, 401)
#
#     token = parts[1]
#     return token
#
#
# def decorated(__request):
#     token = get_token_auth_header_1(__request=__request)
#     jsonurl = urlopen(AUTH0_DOMAIN + "/protocol/openid-connect/certs")
#     jwks = json.loads(jsonurl.read())
#     unverified_header = jwt.get_unverified_header(token)
#     rsa_key = {}
#     for key in jwks["keys"]:
#         if key["kid"] == unverified_header["kid"]:
#             rsa_key = {
#                 "kty": key["kty"],
#                 "kid": key["kid"],
#                 "use": key["use"],
#                 "n": key["n"],
#                 "e": key["e"]
#             }
#     if rsa_key:
#         try:
#             payload = jwt.decode(
#                 token,
#                 rsa_key,
#                 algorithms=ALGORITHMS,
#                 audience=API_AUDIENCE,
#                 issuer=AUTH0_DOMAIN
#             )
#         except jwt.ExpiredSignatureError:
#             raise AuthError({"code": "token_expired",
#                              "description": "token is expired"}, 401)
#         except jwt.JWTClaimsError:
#             raise AuthError({"code": "invalid_claims",
#                              "description":
#                                  "incorrect claims,"
#                                  "please check the audience and issuer"}, 401)
#         except Exception:
#             raise AuthError({"code": "invalid_header",
#                              "description":
#                                  "Unable to parse authentication"
#                                  " token."}, 401)
#         return payload
#     raise AuthError({"code": "invalid_header",
#                      "description": "Unable to find appropriate key"}, 401)