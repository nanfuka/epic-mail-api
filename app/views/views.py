from flask import Flask, jsonify, request, json
from app.controllers.user_controllers import User_controllers
from app.controllers.mail_controller import Mail_controller
from functools import wraps
import jwt
import datetime

from app.validators import Validators
from app.auth import Authentication


app = Flask(__name__)


validators = Validators()
user_controller = User_controllers()
mail_controller = Mail_controller()

authentication = Authentication()


@app.route('/')
def index():
    """route that returns the welcome note or index page"""
    return "welcome to Epic mail Application"


@app.route('/api/v1/auth/signup', methods=['POST'])
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


@app.route('/api/v1/message', methods=['POST'])
@authentication.user_token
def create_message():
    """The loggedin user can create a new email using this route"""
    token = authentication.extract_token_from_header()
    senderid = authentication.decode_user_token_id(token)
    data = request.get_json()
    validate = validators.validate_message_keys('subject',
                                                'message',
                                                'parentMessageId',
                                                'status',
                                                'reciever_id',
                                                'sender_id', list(data.keys()))
    if validate:
        return jsonify({"status": 400, "error": validate})

    subject = data['subject']
    message = data['message']
    parentMessageId = data['parentMessageId']
    reciever_id = data['reciever_id']
    status = data['status']
    sender_id = senderid

    invalid_subject_message_status = validators.validate_subject(
        subject, message, status)
    if invalid_subject_message_status:
        return jsonify({"status": 400, "error": invalid_subject_message_status})

    valid_id = validators.validate_id(parentMessageId, sender_id, reciever_id)
    valid_parentId = validators.get_parentMessageId(parentMessageId)
    if valid_parentId:
        return jsonify({"status": 400, "error": valid_parentId})

    if valid_id:
        return jsonify({"status": 400, "error": valid_id})

    new_mail = mail_controller.create_mail(reciever_id=reciever_id,
                                           sender_id=sender_id,
                                           subject=subject,
                                           message=message,
                                           parentMessageId=parentMessageId,
                                           status=status)
    return jsonify({"status": 201, "data": [new_mail]})
