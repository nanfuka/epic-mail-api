from app.models.users import User, user_list
from app.auth import Authentication
from app.db import Database


import jwt
import datetime
authentication = Authentication()
database = Database()


class UserControllers:
    def signup(self, **kwargs):
        """
        function that appends the registered user to teh users'
         list and returns the user details"""
        user = User(**kwargs)
        new_user = user.get_dictionary()
        user_list.append(new_user)
        id = new_user['id']
        token = authentication.create_user_token(id)
        return {"token": token, "id": new_user['id'], "firstname": new_user['firstname'],
                "lastname": new_user['lastname'], "email": new_user['email']}

    def get_login_email(self, email):
        """function which checks whether an email has beed used before"""
        for user in user_list:
            if user['email'] == email:
                email = user['email']
                return email

    def login(self, email, password):
        """method for logging in the registered user"""
        # id = self.get_login_id(email)
        # if len(user_list) < 1:
        #     return {
        #         "status": 400,
        #         "message":
        #         "there are currently no registered users in the system"}       
        # for user in user_list:
        #     if user['email'] == email and user['password'] == password:
        if database.login(email, password):
            id = database.login(email, password)['id']
            token = authentication.create_user_token(id)    
            return { "status": 200,
                "data": [{"token": token}],
                "message": "you have successfully logged in as a user"}   
            # if user['email'] != email and user['password'] != password:
        # return {"error": "the email and password are invalid"}
        return {
            "status": 400,
            "error": "the email and password you have entered are invalid"}

    def extract_token(self, email, password):
        data = self.login(email, password)
        return data[0]

    def get_login_id(self, email):
        for user in user_list:
            if user['email'] == email:
                id = user['id']
                return id

