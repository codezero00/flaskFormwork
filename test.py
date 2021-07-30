import json
from urllib.request import urlopen
from functools import wraps

from flask import Flask, request, jsonify, _request_ctx_stack
from jose import jwt

from config import AUTH0_DOMAIN, API_IDENTIFIER, ALGORITHMS, API_AUDIENCE

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

token = 'eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJYVEJld2ZzQ0ZlekExVUdOcHF3dnRvdHE4VnZwX3Itd09EV29tNjM2dWlZIn0.eyJleHAiOjE2MjcwNzc1NTIsImlhdCI6MTYyNzA0MTU1MiwiYXV0aF90aW1lIjoxNjI3MDQxNTUyLCJqdGkiOiJlOGMyMjQ5Ny1iY2Y5LTRmN2YtOTUzMi1kZGU3YWQwMDQzZTgiLCJpc3MiOiJodHRwOi8vMTcyLjE2LjQuMTA2OjgwODAvYXV0aC9yZWFsbXMvbWFzdGVyIiwiYXVkIjpbIm1hc3Rlci1yZWFsbSIsImFjY291bnQiXSwic3ViIjoiY2NlZjYwYTMtNDA5Zi00MzkxLWJlZmItNGEzZTY0OTEyYzc4IiwidHlwIjoiQmVhcmVyIiwiYXpwIjoibWljX2xvY2FsaG9zdCIsIm5vbmNlIjoiMGEwMzc3MjYtYjUxMy00MTFhLTgzYjMtYWJlODczM2U0NjEzIiwic2Vzc2lvbl9zdGF0ZSI6IjE2YTA0ZmQ0LTM2MjYtNGYwOC05ZDk2LWU4NGYwMGFiNGYyZSIsImFjciI6IjEiLCJhbGxvd2VkLW9yaWdpbnMiOlsiaHR0cDovL2xvY2FsaG9zdDo2NjUwIl0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJjcmVhdGUtcmVhbG0iLCJvZmZsaW5lX2FjY2VzcyIsImFkbWluIiwidW1hX2F1dGhvcml6YXRpb24iXX0sInJlc291cmNlX2FjY2VzcyI6eyJtYXN0ZXItcmVhbG0iOnsicm9sZXMiOlsidmlldy1pZGVudGl0eS1wcm92aWRlcnMiLCJ2aWV3LXJlYWxtIiwibWFuYWdlLWlkZW50aXR5LXByb3ZpZGVycyIsImltcGVyc29uYXRpb24iLCJjcmVhdGUtY2xpZW50IiwibWFuYWdlLXVzZXJzIiwicXVlcnktcmVhbG1zIiwidmlldy1hdXRob3JpemF0aW9uIiwicXVlcnktY2xpZW50cyIsInF1ZXJ5LXVzZXJzIiwibWFuYWdlLWV2ZW50cyIsIm1hbmFnZS1yZWFsbSIsInZpZXctZXZlbnRzIiwidmlldy11c2VycyIsInZpZXctY2xpZW50cyIsIm1hbmFnZS1hdXRob3JpemF0aW9uIiwibWFuYWdlLWNsaWVudHMiLCJxdWVyeS1ncm91cHMiXX0sImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsInByZWZlcnJlZF91c2VybmFtZSI6InRlc3QifQ.L__lD8POXyacqCxpM2jHYsiVFf0y_XA-l9ML5wSqqu8rSemlCHWCvSyRSzYG4Jc1JOkGggYvZpYWq0ni2Ay2MVNWL7uibqSEuIxBYEG35JWqcqud6W2tUzf2_1Kl5NLrB-NPdHvTP_1f71JWQjDRwpgrDiuhvs0AWJXtsIx5Aiz_EowFoVxfc5AYS0b9TLfLBmQEcGJrbKxOgxFcjekYtClgpIFGts_aj1TnMQHo-0r_qNYpAcMmGkSkWC0zRfvFr2JwmUXKIbD5RfU3GymFDCV3EUYTJHlvU09_v8kNegt7V7xlcrrVBG4i5QpJ4i3dScGNaAw67w8_6uE9n-HJXA'

# print(jwt.decode(token))

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
            # rsa_key,
            algorithms=ALGORITHMS,
            audience=API_AUDIENCE,
            issuer=AUTH0_DOMAIN
        )
    except jwt.ExpiredSignatureError
        print(AuthError({"code": "token_expired","description": "token is expired"}, 401))
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


    print(payload, 'payload')
raise AuthError({"code": "invalid_header",
                 "description": "Unable to find appropriate key"}, 401)