from app.models.users import User, user_list
from app.auth import Authentication

import jwt
import datetime
authentication = Authentication()


class User_controllers:
    def signup(self, **kwargs):
        """
        function that appends the registered user to teh users'
         list and returns the user details"""
        user = User(**kwargs)
        newuser = user.get_dictionary()
        user_list.append(newuser)
        id = newuser['id']
        token = authentication.create_user_token(id)
        return {"token": token, "id": newuser['id'], "firstname": newuser['firstname'],
                "lastname": newuser['lastname'], "email": newuser['email']}

    def get_login_email(self, email):
        """function which checks whether an email has beed used before"""
        for user in user_list:
            if user['email'] == email:
                email = user['email']
                return email

    def login(self, email, password):
        """method for logging in the registered user"""
        id = self.get_login_id(email)
        if len(user_list) < 1:
            return {
                "status": 200,
                "message":
                "there are currently no registered users in the system"}       
        for user in user_list:
            if user['email'] == email and user['password'] == password:
                token = authentication.create_user_token(id)    
                return {
                    "data": [{"token": token}],
                    "message": "you have successfully logged in as a user"}   
            if user['email'] != email and user['password'] != password:
                return {"error": "the email and password are invalid"}
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

    # def validate_login_keys(self, email, password, data):
    #     if email not in data:
    #         return "Enter email field"
    #     if password not in data:
    #         return "Enter password field"
