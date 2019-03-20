import jwt
import datetime
from functools import wraps
from flask import Flask, jsonify, request, json


class Authentication:
    def create_user_token(self, id):
        """function that creates the users token"""

        token = jwt.encode({'id': id,
                            'exp': datetime.datetime.utcnow(
                            ) + datetime.timedelta(minutes=30)},
                           "mylovelydaughters")
        return token.decode('utf-8')

    def create_admin_token(self, user_id):
        """function which creates teh admins token"""

        token = jwt.encode({'user_id': user_id, "isAdmin": "true",
                            'exp': datetime.datetime.utcnow(
                             ) + datetime.timedelta(minutes=30)}, "amanadmin")
        return token.decode('utf-8')

    def user_token(self, f):
        """function for creating a user token decorator"""
        @wraps(f)
        def _verify(*args, **kwargs):
            auth_headers = request.headers.get('Authorization', '').split()
            try:
                token = auth_headers[1]
                print(token)
                if not token:
                    error = jsonify({'message': 'Token is missing'}), 403
                data = jwt.decode(token, "mylovelydaughters")
                return f(*args, **kwargs)
            except IndexError:
                error = jsonify({
                    "message": "Token does not exist",
                    "authenticated": False
                }), 401
            except jwt.DecodeError:
                error = jsonify({
                    "message": "Token Decode Failed!",
                    "authenticated": False
                }), 401
            except jwt.ExpiredSignatureError:
                error = jsonify({
                    'message': 'Expired token. Please Log In again.',
                    'authenticated': False
                }), 401
            except jwt.InvalidTokenError:
                error = jsonify({
                    'message': 'Invalid token. Please Log In again',
                    'authenticated': False
                }), 401
            return error

        return _verify

    def admin_token(self, f):
        """function for creating the admin token decorator"""
        @wraps(f)
        def _verify(*args, **kwargs):
            auth_headers = request.headers.get('Authorization', '').split()
            try:
                token = auth_headers[1]
                print(token)
                if not token:
                    error = jsonify({'message': 'Token is missing'}), 403
                data = jwt.decode(token, "amanadmin")
                return f(*args, **kwargs)
            except IndexError:
                error = jsonify({
                    "message": "Token does not exist",
                    "authenticated": False
                }), 401
            except jwt.DecodeError:
                error = jsonify({
                    "message": "Token Decode Failed!",
                    "authenticated": False
                }), 401
            except jwt.ExpiredSignatureError:
                error = jsonify({
                    'message': 'Expired token. Please Log In again.',
                    'authenticated': False
                }), 401
            except jwt.InvalidTokenError:
                error = jsonify({
                    'message': 'Invalid token. Please Log In again',
                    'authenticated': False
                }), 401
            return error

        return _verify

    def extract_token_from_header(self):
        """Method for extracting the token from header"""
        """Get token from the headers"""
        authorization_header = request.headers.get("Authorization")
        if not authorization_header or "Bearer" not in authorization_header:
            return jsonify({
                "error": "Bad authorization header",
                "status": 400
            })
        token = authorization_header.split(" ")[1]
        return token

    def decode_user_token_id(self, token):
        """Method for retrieving an id from the token"""
        """ Method to return the token to its readable state """
        decoded = jwt.decode(token, 'mylovelydaughters', algorithms="HS256")
        return decoded['id']
