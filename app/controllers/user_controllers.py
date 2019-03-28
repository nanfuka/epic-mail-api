from app.auth import Authentication
from app.db import Database


import jwt
import datetime
authentication = Authentication()
database = Database()


class UserControllers:
    def login(self, email, password):
        """method for logging in the registered user"""
        if database.login(email, password):
            id = database.login(email, password)['id']
            token = authentication.create_user_token(id)    
            return {"status": 200,
                "data": [{"token": token}],
                "message": "you have successfully logged in as a user"}   
        return {
            "status": 400,
            "error": "the email and password you have entered are invalid"}