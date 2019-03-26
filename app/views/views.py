from flask import Flask, jsonify, request, json
from app.controllers.user_controllers import UserControllers
from app.controllers.mail_controllers import MailController
from functools import wraps
import jwt
import datetime
from flasgger import Swagger, swag_from
from app.db import Database
from app.validators import Validators
from app.auth import Authentication
import datetime

app = Flask(__name__)

swagger = Swagger(app)
validators = Validators()
user_controller = UserControllers()
mail_controller = MailController()
database = Database()

authentication = Authentication()


@app.route('/')
@swag_from('../apidocs/index.yml', methods=['GET'])
def index():
    """route that returns the welcome note or index page"""
    return "welcome to the Epic mail Application "


@app.route('/api/v2/auth/signup', methods=['POST'])
@swag_from('../apidocs/signup.yml', methods=['POST'])
def signup():
    """route for registering a new user of teh application"""
    data = request.get_json()

    validate = validators.validate_signup_keys(
        'firstname', 'lastname', 'email', 'password', list(data.keys()))
    if validate:
        return jsonify({"status": 400, "error": validate})
    firstname = data['firstname']
    lastname = data['lastname']
    email = data['email']
    password = data['password']

    error_name = validators.validate_names(
        firstname=firstname,
        lastname=lastname)
    error_email = validators.validate_email(email)
    error_password = validators.validate_password(password)

    if error_name:
        return jsonify({"status": 404, "error": error_name})
    if error_email:
        return jsonify({"status": 404, "error": error_email})
    if error_password:
        return jsonify({"status": 404, "error": error_password})
    register = database.signup(firstname=firstname,
                                      lastname=lastname,
                                      email=email,
                                      password=password)
    token = authentication.create_user_token(register['id'])                                  
    return jsonify({"status": 201,
                    "data": [{"token": token, "user": register}],
                    "message": "thanks for registering with Epic mail"})


@app.route('/api/v2/auth/login', methods=['POST'])
@swag_from('../apidocs/login.yml', methods=['POST'])
def login():
    """
    route for logging in only the registered user but 
    submitting the correct email and password
    """
    data = request. get_json()

    validate_login_keys = validators.validate_login_keys(
        'email',
        'password',
        list(data.keys()))
    if validate_login_keys:
        return jsonify({"status": 400, "error": validate_login_keys})
    email = data['email']
    password = data['password']
    invalid_login_values = validators.validate_login_values(email, password)
    if invalid_login_values:
        return jsonify({"status": 404, "error": invalid_login_values})
    login = user_controller.login(email, password)
    if login:
        return jsonify(login)


def get_id_from_header():
    token = authentication.extract_token_from_header()
    senderid = authentication.decode_user_token_id(token)
    return senderid


@app.route('/api/v2/message', methods=['POST'])
@authentication.user_token
@swag_from('../apidocs/message.yml', methods=['POST'])

def create_message():
    """The loggedin user can create a new email using this route"""
    token = authentication.extract_token_from_header()
    senderid = authentication.decode_user_token_id(token)
    data = request.get_json()
    validate = validators.validate_message_keys('subject',
                                                'message',
                                                'status',
                                                'reciever_id',
                                                'parent_message_id',
                                                list(data.keys()))
    if validate:
        return jsonify({"status": 400, "error": validate})

    created_on = datetime.datetime.now()
    subject = data['subject']
    message = data['message']
    status = data['status']
    sender_id= senderid 
    reciever_id = data['reciever_id']
    # created_mail =database.create_message(created_on=created_on, subject=subject, message=message, status=status, sender_id=sender_id, reciever_id=reciever_id)
    # return jsonify(created_mail)
    


    invalid_subject_message_status = validators.validate_subject(
        subject, message, status)
    if invalid_subject_message_status:
        return jsonify({
            "status": 400,
            "error": invalid_subject_message_status})


    valid_id = validators.validate_id(reciever_id)
    if valid_id:
        return jsonify({"status": 400, "error": valid_id})
    
    new_mail = database.create_message(
                                        created_on=created_on,
                                           
                                           subject=subject,
                                           message=message,
                                           status=status,
                                           sender_id=sender_id, 
                                           reciever_id=reciever_id
                                           )
    if status == "sent":
        inbox = database.create_inbox(created_on=created_on, subject=subject, message=message, sender_id=sender_id, reciever_id=reciever_id, parent_message_id=new_mail['id'], status=status)
    return jsonify({"status": 201, "data":[{"id":new_mail['id'], "created_on":new_mail['created_on'], "subject": new_mail['subject'], "message":new_mail['message'], "parent_message_id":new_mail['id'], "status":new_mail['status'] }]})

@app.route('/api/v1/messages/sent', methods=['GET'])
@authentication.user_token
@swag_from('../apidocs/sent.yml', methods=['GET'])
def get_sent_mail():
    
    """Route which fetches all mail sent by the current user"""
    sender_id = get_id_from_header()
    
    return jsonify({"status": 200, "data": database.get_all_sent_mail_by_a_user(sender_id)})

@app.route('/api/v2/modify_status/<int:message_id>', methods=['PATCH'])
@authentication.user_token
@swag_from('../apidocs/sent.yml', methods=['GET'])
def modify_message(message_id):
    
    """the current user can modify the status of their message"""
    reciever_id = get_id_from_header()
    data = request.get_json()
    status = data.get('status')
    modified = database.modify_message_status(status, reciever_id, message_id)
    return jsonify({"status": 200, "data":
                    [{"id": message_id,
                        "message": "successfully modified the status"}]})




@app.route('/api/v2/messages', methods=['GET'])
@authentication.user_token
@swag_from('../apidocs/recieved.yml', methods=['GET'])

def get_recieved_mail():
    """
    reciever can view all mail sent to them marked
     sent with a recieverid of logged in user
    """
    reciever_id = get_id_from_header()
    return jsonify ({"status": 200, "data":database.get_induviduals_inbox(reciever_id)})

# @app.route('/api/v2/messages/unread', methods=['GET'])
# @authentication.user_token
# @swag_from('../apidocs/unread.yml', methods=['GET'])

# def get_unread_mail():

#     """
#     view all messages whose status is sent to a particular reciever-id
#     """
#     reciever_id = get_id_from_header()
#     return jsonify (database.get_unread_mail_from_inbox(reciever_id))


@app.route('/api/v1/messages/deleted/<int:message_id>', methods=['DELETE'])
@authentication.user_token
@swag_from('../apidocs/unread.yml', methods=['GET'])

def get_delete_mail(message_id):

    """
    view all messages whose status is sent to a particular reciever-id
    """
    reciever_id = get_id_from_header()
    delete = database.delete_mail(message_id, reciever_id)
    
    return jsonify({"status":200, "message":"The email has been deleted successfully"})
    

@app.route('/api/v1/messages/<int:message_id>', methods=['GET'])
@authentication.user_token
@swag_from('../apidocs/unread.yml', methods=['GET'])

def get_particular_mail(message_id):

    """Route for retrieving a particular mail"""

    reciever_id = get_id_from_header()
    return jsonify(database.get_get_particular_message(message_id, reciever_id))

