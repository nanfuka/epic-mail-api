from app.auth import Authentication
from app.controllers.mail_controllers import Mail
import jwt
import datetime
authentication = Authentication()
mail = Mail()


class UserControllers:
    def login(self, email, password):
        """method for logging in the registered user"""
        if mail.login(email, password):
            id = mail.login(email, password)['id']
            token = authentication.create_user_token(id)    
            return {"status": 200,
                    "data": [{"token": token}],
                    "message": "you have successfully logged in as a user"}   
        return {
            "status": 400,
            "error": "the email and password you have entered are invalid"}