from flask import Flask, jsonify, request, json
from app.controllers.user_controllers import UserControllers
from app.controllers.mail_controllers import Mail
from functools import wraps
import jwt
import datetime
from flasgger import Swagger, swag_from
from app.validators import Validators
from app.auth import Authentication
import datetime

app = Flask(__name__)

swagger = Swagger(app)
validators = Validators()
user_controller = UserControllers()
mail = Mail()
authentication = Authentication()

app = Flask(__name__)


@app.route('/')
@swag_from('../apidocs/index.yml', methods=['GET'])
def index():
    """route that returns the welcome note or index page"""
    return jsonify({"message":"welcome to the Epic mail Application "})


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
        return jsonify({"status": 400, "error": error_name})
    if error_email:
        return jsonify({"status": 400, "error": error_email})
    if error_password:
        return jsonify({"status": 400, "error": error_password})
    register = mail.signup(firstname=firstname,
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
        return jsonify({"status": 400, "error": invalid_login_values})
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
    """The loggedin user can create a new mail using this route"""
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
    sender_id = senderid
    reciever_id = data['reciever_id']

    invalid_subject_message_status = validators.validate_subject(
        subject, message, status)
    if invalid_subject_message_status:
        return jsonify({
            "status": 400,
            "error": invalid_subject_message_status})

    valid_id = validators.validate_id(reciever_id)
    if valid_id:
        return jsonify({"status": 400, "error": valid_id})
    new_mail = mail.create_message(
        created_on=created_on,

        subject=subject,
        message=message,
        status=status,
        sender_id=sender_id,
        reciever_id=reciever_id
    )
    if status == "sent":
        inbox = mail.create_inbox(created_on=created_on,
                                  subject=subject,
                                  message=message,
                                  sender_id=sender_id,
                                  reciever_id=reciever_id,
                                  parent_message_id=new_mail['id'],
                                  status=status)
    return jsonify({"status": 201,
                    "data": [{"id": new_mail['id'],
                              "created_on":new_mail['created_on'],
                              "subject": new_mail['subject'],
                              "message":new_mail['message'],
                              "parent_message_id":new_mail['id'],
                              "status":new_mail['status']}]})


@app.route('/api/v2/messages/sent', methods=['GET'])
@authentication.user_token
@swag_from('../apidocs/sent.yml', methods=['GET'])
def get_sent_mail():
    """Route which fetches all mail sent by the current user"""
    sender_id = get_id_from_header()
    if mail.get_all_sent_mail_by_a_user(sender_id):
        return jsonify({"status": 200,
                       "data": mail.get_all_sent_mail_by_a_user(sender_id)})
    return jsonify({"status": 404, "error": "you have no sent mails"})


@app.route('/api/v2/messages', methods=['GET'])
@authentication.user_token
@swag_from('../apidocs/recieved.yml', methods=['GET'])
def get_recieved_mail():
    """
    reciever can view all mail sent to them marked
     sent with a recieverid of logged in user
    """
    reciever_id = get_id_from_header()
    inbox = mail.get_induviduals_inbox(reciever_id)
    if inbox:
        return jsonify({"status": 200,
                        "data": inbox})
    return jsonify({"status": 404, "error": "you have no recieved messages"})


@app.route('/api/v2/messages/unread', methods=['GET'])
@authentication.user_token
@swag_from('../apidocs/unread.yml', methods=['GET'])
def get_unread_mail():
    """
    view all messages in the inbox whose status is not read
    """
    reciever_id = get_id_from_header()
    status = "unread"
    unread = mail.get_unread_mail_from_inbox(status, reciever_id)
    if unread:
        return jsonify({"status": 200, "data": unread})

    return jsonify({
        "status": 404,
        "message": "you do not have any unread mail in your inbox"
    })


@app.route('/api/v2/messages/deleted/<int:message_id>', methods=['DELETE'])
@authentication.user_token
@swag_from('../apidocs/unread.yml', methods=['GET'])
def get_delete_mail(message_id):
    """
    delete a particular email
    """
    reciever_id = get_id_from_header()
    delete = mail.delete_mail(message_id, reciever_id)
    if mail.check_if_message_id_exists(message_id):
        delete
        return jsonify({
            "status": 200,
            "data": [{"message":
                      "The email has been deleted successfully"}]})
    return jsonify({
        "status": 404,
        "message": "the message with supplied message_id is not available"})


@app.route('/api/v2/messages/<int:message_id>', methods=['GET'])
@authentication.user_token
@swag_from('../apidocs/unread.yml', methods=['GET'])
def get_particular_mail(message_id):
    """Route for retrieving a particular mail"""

    reciever_id = get_id_from_header()
    particular_mail = mail.get_particular_message(message_id, reciever_id)
    if mail.check_if_message_id_exists(message_id):
        if particular_mail:
            return jsonify({"status": 200, "data": [particular_mail]})
        return jsonify({
            "status": 404,
            "message": "the message with supplied message_id is not available"
        })
    return jsonify({
        "status": 404,
        "error": "message_id is not in the system"})


@app.route('/api/v2/groups', methods=['POST'])
@authentication.user_token
def create_group():
    """With this route, a logged in user can create a new 
    group and become the owner of that group
    """
    admin = get_id_from_header()
    data = request.get_json()
    name = data.get('name')
    role = data.get('role')
    admin = admin
    invalid = validators.validate_group_creation(name=name, role=role)
    if invalid:
        return jsonify({"status": 400, "error": invalid})
    new_group = mail.create_groups(admin, name, role)

    return jsonify({"status": 201, "data": [new_group]})


@app.route('/api/v2/groups', methods=['GET'])
@authentication.user_token
def fetch_groups():
    """The logged in user can view all the 
    groups that they have created 
    """
    admin = get_id_from_header()
    all_groups = mail.fetch_all_groups(admin)
    if all_groups:
        return jsonify({"status": 200, "data": all_groups})
    return jsonify({"status": 404,
                    "error": "You have not yet created any groups"})


@app.route('/api/v2/groupss/<int:group_id>', methods=['DELETE'])
@authentication.user_token
def delete_groups(group_id):
    """
    the admin of the group can delete
    the group with a particular group_id
    """
    admin = get_id_from_header()
    valid_group_id = mail.check_if_group_id_exists(group_id)
    if valid_group_id:
        delete = mail.delete_particular_groups(group_id, admin)
        return jsonify({
            "status": 200,
            "data": [{"message": "The group has been deleted"}]})
    return jsonify({
        "status": 404,
        "error": "the group with the supplied group_id is not in the system"})


@app.route('/api/v2/groups/<int:group_id>/name', methods=['PATCH'])
@authentication.user_token
def change_group_name(group_id):
    """Admin can change the name of the group"""
    admin = get_id_from_header()

    valid_group_id = mail.check_if_group_id_exists(group_id)
    if valid_group_id:
        if mail.get_admin_of_a_group(group_id) == get_admin_json(admin):

            data = request.get_json()
            name = data.get('name')
            invalid_name = validators.validate_modify(name)
            if invalid_name:
                return jsonify({"status": 400, "message": invalid_name})
            change = mail.patch_group_name(group_id, name)
            if change:
                return jsonify({"status": 200, "data": change})
        return jsonify({
            "status": 400,
            "error": "you can only modify a group which you created"})
    return jsonify({"status": 404,
                    "error": "the group is not available"})


def get_admin_json(admin):
    admin = get_id_from_header()
    return {"admin": str(admin)}


@app.route('/api/v2/groups/<int:group_id>/users', methods=['POST'])
@authentication.user_token
def adduser_to_group(group_id):
    """An admin can add members to a group which they created"""
    admin = get_id_from_header()

    valid_group_id = mail.check_if_group_id_exists(group_id)
    if valid_group_id:
        if mail.get_admin_of_a_group(group_id) == get_admin_json(admin):

            data = request.get_json()
            group_id = group_id
            userid = data.get('userid')
            userrole = data.get('userrole')

            invalid_inputs = validators.validate_add_user_to_group(
                userid, userrole)
            if invalid_inputs:
                return jsonify({"status": 400, "error": invalid_inputs})

            add_user = mail.create_group(group_id, userid, userrole)
            all_members_of_this_group = mail.get_all_group_members(
                group_id)
            return jsonify({"status": 201, "data": all_members_of_this_group})
        return jsonify({
            "status": 404,
            "error": "you can only modify a group which you created"})
    return jsonify({"status": 404, "error": "the group is non existant"})


@app.route('/api/v2/groups/<int:group_id>/users/<int:user_id>',
           methods=['DELETE'])
@authentication.user_token
def delete_user_from_particular_group(group_id, user_id):
    """Route to delete a particular user from the group"""
    admin = get_id_from_header()
    valid_group_id = mail.check_if_group_id_exists(group_id)
    if valid_group_id:
        if mail.get_admin_of_a_group(group_id) == get_admin_json(admin):

            delete_user_from_group = mail.delete_user_from_specific_group(
                user_id, group_id)
            return jsonify({
                "status": 200,
                "data": "The user has been deleted from the group"})
        return jsonify({
            "status": 403,
            "error": "You are not authorised to modify this group"})
    return jsonify({"status": 404, "error": "the group is non existant"})


@app.route('/api/v2/groups/<int:group_id>/messages', methods=['POST'])
@authentication.user_token
def create_group_message(group_id):
    """
    The loggedin user can create a new mail
      and send it to the group using this route
    """
    admin = get_id_from_header()
    valid_group_id = mail.check_if_group_id_exists(group_id)
    if valid_group_id:
        if mail.get_admin_of_a_group(group_id) == get_admin_json(admin):
            admin = get_id_from_header()
            data = request.get_json()
            created_on = datetime.datetime.now()
            subject = data['subject']
            message = data['message']
            status = data['status']
            sender_id = admin
            group_id = group_id

            invalid_data = validators.validate_group_mails(
                subject, message, status)
            if invalid_data:
                return jsonify({"status": 400, "message": invalid_data})

            new_mail = mail.create_groupmessage(
                created_on=created_on,

                subject=subject,
                message=message,
                status=status,
                sender_id=sender_id,

                group_id=group_id
            )
            return jsonify({"status": 201,
                            "data": [{"id": new_mail['id'],
                                      "createdOn":new_mail['created_on'],
                                      "subject":new_mail['subject'],
                                      "message":new_mail['message'],
                                      "parentMessageId":new_mail['id'],
                                      "status":new_mail['status']}]})
        return jsonify({
            "status": 403,
            "error": "you are not authosrised to modify this group"
        })
    return jsonify({"status": 404, "error": "the group is non existant"})
