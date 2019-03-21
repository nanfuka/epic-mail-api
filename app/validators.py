import re
from app.controllers.user_controllers import User_controllers
from app.models.users import user_list
from app.models.mail import mail_list

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

    # def validate_signup_keys(self, *args):
    #     """function to validate all the message keys"""
    #     firstname = args[0]
    #     lastname = args[1]
    #     email = args[2]
    #     password = args[3]
    #     lst = args[4]
    #     if firstname not in lst:
    #         return 'firstname field must be present'

    #     if lastname not in lst:
    #         return 'lastname field must be present'

    #     if email not in lst:
    #         return 'email field must be present'

    #     if password not in lst:
    #         return 'password field must be present'

    # def validate_login_keys(self, email, password, data):
    #     if email not in data:
    #         return "Enter email field"
    #     if password not in data:
    #         return "Enter password field"

    def validate_login_values(self, email, password):
        if not password:
            return "Enter your password"
        if not email:
            return "Enter your email"

    def validate_subject(self, subject, message, status):
        """Function which validates message and status"""
        if not subject or subject.strip() == "":
            return "please enter the subject of your message"
        if not message or message.strip() == "":
            return "please enter your message"
        if len(subject) < 5:
            return " the subject of the mail is too short"
        if len(subject) > 100:
            return " the subject line is too long,\
                write your message in the message box"
        if status != "sent" and status != "read" and status != "draft":
            return "status should either be sent, read or draft"

    def validate_id(self, parentMessageId, sender_id, reciever_id):
        """function which validates the ids passed upon posting a message"""
        if not sender_id:
            return "Enter sender_id"
        if not isinstance(sender_id, int):
            return "sender_id should be a number"

        if not isinstance(reciever_id, int):
            return "reciever_id should be a number"
        if not isinstance(parentMessageId, int):
            return "parentMessageId should be a number"
        for mail in mail_list:
            if mail['reciever_id']!= reciever_id:
                return "The submited reciever_id is not registered with the application.\
                     please enter a valid reciever_id"

        for mail in mail_list:
            if mail['sender_id']!= sender_id:
                return 
                "The submited sender_id is not registered with the application."
        if not isinstance(parentMessageId, int):
            return "The parentMessageid should be an integer"

        if not reciever_id:
            return "Enter the reciever id please"
        if not isinstance(reciever_id, int):
            return "The reciever_id should be an number"


    def get_parentMessageId(self, parentMessageId):
        """Functiont to check for validity of the parent message-id"""

        if len(mail_list)>1:
            for mail in mail_list:
                if mail['parentMessageId']!=parentMessageId:
                    return "the parent message_id is not in the system"
    
    def validate_message_keys(self, *args):
        """function to validate all the message keys"""
        subject = args[0]
        message = args[1]
        parentMessageId = args[2]
        status = args[3]
        reciever_id = args[4]
        sender_id = args[5]
        lst = args[6]
        if subject not in lst:
            return {'message': 'subject field must be present'}

        if message not in lst:
            return {'message': 'message field must be present'}

        if parentMessageId not in lst:
            return {'message': 'parentMessageId field must be present'}

        if status not in lst:
            return {'message': 'status field must be present'}

        if reciever_id not in lst:
            return {'message': 'reciever_id field must be present'}

        if sender_id not in lst:
            return {'message': 'sender_id field must be present'}
    
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

