from flask import Flask, jsonify, request, json
from app.controllers.user_controllers import User_controllers
from app.controllers.mail_controller import Mail_controller
from functools import wraps
import jwt
import datetime
from flasgger import Swagger, swag_from

from app.validators import Validators
from app.auth import Authentication


app = Flask(__name__)

swagger = Swagger(app)
validators = Validators()
user_controller = User_controllers()
mail_controller = Mail_controller()

authentication = Authentication()


@app.route('/')
@swag_from('../apidocs/index.yml', methods=['GET'])
def index():
    """route that returns the welcome note or index page"""
    return "welcome to Epic mail Application"


@app.route('/api/v1/auth/signup', methods=['POST'])
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
    register = user_controller.signup(firstname=firstname,
                                      lastname=lastname,
                                      email=email,
                                      password=password)
    return jsonify({"status": 201,
                    "data": [register],
                    "message": "thanks for registering with Epic mail"})


@app.route('/api/v1/auth/login', methods=['POST'])
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


@app.route('/api/v1/message', methods=['POST'])
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
                                                list(data.keys()))
    if validate:
        return jsonify({"status": 400, "error": validate})

    subject = data['subject']
    message = data['message']
    reciever_id = data['reciever_id']
    status = data['status']
    sender_id = senderid

    invalid_subject_message_status = validators.validate_subject(
        subject, message, status)
    if invalid_subject_message_status:
        return jsonify({
            "status": 400,
            "error": invalid_subject_message_status})

    valid_id = validators.validate_id(reciever_id)
    if valid_id:
        return jsonify({"status": 400, "error": valid_id})

    new_mail = mail_controller.create_mail(reciever_id=reciever_id,
                                           sender_id=senderid,
                                           subject=subject,
                                           message=message,
                                           status=status)
    return jsonify({"status": 201, "data": [new_mail]})


@app.route('/api/v1/messages/sent', methods=['GET'])
@authentication.user_token
def get_sent_mail():
    
    """Route which fetches all mail sent by the current user"""
    sender_id = senderid = get_id_from_header()
    return jsonify(mail_controller.get_all_mail_sent_by_a_user(sender_id))


@app.route('/api/v1/messages', methods=['GET'])
@authentication.user_token
def get_recieved_mail():
    """
    reciever can view all mail sent to them marked
     sent with a recieverid of logged in user
    """
    # token = authentication.extract_token_from_header()
    # reciever_id = authentication.decode_user_token_id(token)
    reciever_id = get_id_from_header()
    return jsonify(
        mail_controller.get_all_recieved_messages_of_a_user(reciever_id))


@app.route('/api/v1/messages/unread', methods=['GET'])
@authentication.user_token
def get_unread_mail():

    """
    view all messages whose status is sent to a particular reciever-id
    """
    token = authentication.extract_token_from_header()
    reciever_id = authentication.decode_user_token_id(token)
    # reciever_id = get_id_from_header()
    return jsonify(mail_controller.get_all_unread_mail_for_a_user(reciever_id))


@app.route('/api/v1/messages/<int:message_id>', methods=['GET'])
def get_particular_mail(message_id):
    """Route for retrieving a particular mail"""
    return jsonify(mail_controller.get_specific_users_email(message_id))


@app.route('/api/v1/messages/deleted/<int:message_id>', methods=['DELETE'])
def delete_particular_mail(message_id):
    """Route for deleting a particular mail"""
    return jsonify(mail_controller.delete_specific_users_email(message_id))







