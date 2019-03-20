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
        return {"firstname": newuser['firstname'],
                "lastname": newuser['lastname'], "email": newuser['email']}

    def get_login_email(self, email):
        """function which checks whether an email has beed used before"""
        for user in user_list:
            if user['email'] == email:
                email = user['email']
                return email
