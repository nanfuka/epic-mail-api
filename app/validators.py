import re
from app.controllers.user_controllers import User_controllers
from app.models.users import user_list

user_controller = User_controllers()


class Validators:
    def validate_names(self, firstname, lastname):
        """Function to validate names"""
        if not firstname or firstname.strip() == "":
            return "please enter the firstname"

        if not firstname.isalpha():
            return "firstname should only be made up of letters"
        if len(lastname) < 3 and len(lastname) > 3:
            return "invalid lastname. its too short"

        if len(firstname) < 3 and len(firstname) > 1:
            return "invalid firstname. its too short"

        if not lastname or lastname.strip() == "":
            return "please enter the lastname"
        if not lastname.isalpha():
            return "lastname should only be made up of letters"

    def validate_password(self, password):
        """Function to validate a password"""
        if not password or password.strip() == "":
            return "please enter your password"
        if len(password) < 5:
            return "weak password, please increase password strength"

    def validate_email(self, email):
        """function to validate an email"""
        email_validation = re.compile(
            "(^[a-zA-Z0-9_.]+@[a-zA-Z0-9_.]+\.[a-z]+$)")
        if not email or email.strip() == "":
            return "please enter the email"
        if not email_validation.match(email):
            return 'Invalid email, it should be in this format; kals@gma.com'
        if user_controller.get_login_email(email):
            return "the email you have chosen is already in use"

    def validate_signup_keys(self, *args):
        """function to validate all the message keys"""
        firstname = args[0]
        lastname = args[1]
        email = args[2]
        password = args[3]
        lst = args[4]
        if firstname not in lst:
            return 'firstname field must be present'

        if lastname not in lst:
            return 'lastname field must be present'

        if email not in lst:
            return 'email field must be present'

        if password not in lst:
            return 'password field must be present'

    def validate_login_keys(self, email, password, data):
        if email not in data:
            return "Enter email field"
        if password not in data:
            return "Enter password field"

    def validate_login_values(self, email, password):
        if not password:
            return "Enter your password"
        if not email:
            return "Enter your email"
