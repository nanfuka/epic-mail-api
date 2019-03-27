import re
from app.controllers.user_controllers import UserControllers
from app.models.users import user_list
from app.models.mail import mail_list
from app.db import Database
user_controller = UserControllers()
db = Database()


class Validators:
    def validate_names(self, firstname, lastname):
        """Function to validate names"""
        if not firstname or firstname.strip() == "":
            return "please enter the firstname"

        if not firstname.isalpha():
            return "firstname should only be made up of letters"

        if not lastname or lastname.strip() == "":
            return "please enter the lastname"
        if len(lastname) < 3:
            return "invalid lastname. its too short"
        if len(firstname) < 3:
            return "invalid firstname. its too short"

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
        if db.check_email(email):
            return "the email you have chosen is already in use"

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
            return " the subject line is too long"
        if status != "sent" and status != "read" and status != "draft":
            return "status should either be sent, read or draft"

    def validate_id(self, reciever_id):
        """function which validates the ids passed upon posting a message"""
        user_list = db.get_all_users()
        if not isinstance(reciever_id, int):
            return "reciever_id should be a number"

        for mail in mail_list:
            if mail['reciever_id'] != reciever_id:
                return "The submited reciever_id is not registered with the application.\
                     please enter a valid reciever_id"

        # if not isinstance(parentMessageId, int):
        #     return "The parentMessageid should be an integer"

        if not reciever_id:
            return "Enter the reciever id please"
        if not isinstance(reciever_id, int):
            return "The reciever_id should be an number"

    def get_all_read_mail(self):
        read = []
        for mail in mail_list:
            if mail['status'] == 'read':
                read.append(mail)
        return read

    def validate_message_keys(self, *args):
        """function to validate all the message keys"""
        subject = args[0]
        message = args[1]

        status = args[2]
        reciever_id = args[3]
        parent_message_id = args[4]

        lst = args[5]
        if subject not in lst:
            return {'message': 'subject field must be present'}

        if message not in lst:
            return {'message': 'message field must be present'}

        if status not in lst:
            return {'message': 'status field must be present'}

        if reciever_id not in lst:
            return {'message': 'reciever_id field must be present'}

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

    # def get_specific_users_email(self, mail_id, reciever_id):
    #     """Function that retrieves a particular mail"""

    #     for mail in mail_list:

    #         if mail['id'] != mail_id:
    #             return {
    #                 "status": 200,
    #                 "message": "There isnt any mail with the given mail_id"}
    #         if mail['id'] == mail_id and mail['reciever_id'] == reciever_id:
    #             return {"status": 200, "data": [mail]}
    #     if not mail_list:
    #         return {"status": 200,
    #                 "message": "There isn't any mail in the inbox"}
    def validate_parent_message_id(self, parent_message_id, message_id):
        mail_list = db.get_all_mails()
        if parent_message_id != massage_id:
            return "invalid parent_message_id"
        # if not mail_list:
        #     parent_message_id ==1
        # for mail in mail_list:

        #     if mail['id'] == parent_message_id:
        #         print ("invalid")
        # if not mail:
            return "invalid"
        # if not mail:
        #     return "invalid parent"
        # if not mail_list:
        #     parent_message_id ==1

        # if not parent_message_id:
        #     return "please enter teh parnt "
    def validate_group_creation(self, **kwargs):
        name = kwargs.get('name')
        role = kwargs.get('role')
        if isinstance(name, int):
            return "name should be made up of letters"
        if not name or name.strip() == "":
            return"Enter name"
        if not name.isalpha():
            return "name should be made up of letters"
        if db.get_all_groupnames(name):
            return "Name of group already taken, choose anotherone"

        if isinstance(role, int):
            return "role should be made up of letters"
        if not role or role.strip() == "":
            return"Enter role"
        if not role.isalpha():
            return "role should be made up of letters"
        if len(name) < 2:
            return "name is too short"
        if len(role) < 2:
            return "role value is too short"
    
    def validate_group_id(self, group_id):
        if not db.check_if_group_id_exists(group_id):
            return jsonify({"status": 404, "error": "the id you want to delete is not in the system"})

    def validate_modify(self, name):
        if isinstance(name, int):
            return "name should be made up of letters"
        if not name or name.strip() == "":
            return"Enter name"
        if not name.isalpha():
            return "name should be made up of letters"
        if db.get_all_groupnames(name):
            return "Name of group already taken, choose anotherone"
        if len(name) < 2:
            return "name is too short"
    def validate_add_user_to_group(self, user_id, userrole):
        if not user_id:
            return "Enter user_id"
        if not isinstance(user_id, int):
            return "The user_id should be a number"
        if not db.check_user_available(user_id):
            return "The user with that user_id is not registered with the application"
        if not userrole:
            return "Enter userrole"
        if not isinstance(userrole, str):
            return "User role should be a string"
        if len(userrole)<2:
            return "Enter a clear to understand userrole"

    def validate_group_mails(self, subject, message, status):
        if isinstance(subject, int):
            return "subject should be made up of letters"
        if not subject or subject.strip() == "":
            return"Enter name"
        if not subject.isalpha():
            return "subject should be made up of letters"
        if len(subject) < 10:
            return "subject is too short"


        if isinstance(message, int):
            return "message should be made up of letters"
        if not message or message.strip() == "":
            return"Enter message"
        if len(message) < 2:
            return "subject is too short"

        if status != "draft" or status =="sent":
            return "status should of mail should either be sent or in draft"
            