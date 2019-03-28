from app.db import Database
from app.views.views import app
import unittest
import json

database = Database()


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()

    def tearDown(self):
        database.drop_table('groupmessages')
        database.drop_table('groupmembers')
        database.drop_table('sent')
        database.drop_table('inbox')       
        database.drop_table('epicgroups')
        database.drop_table('clusters')
        database.drop_table('messages')
        database.drop_table('users')

        database.create_tables()

    def get_index_page(self):
        """
        Function to create an index page
        """
        return self.client.get('/',
                               content_type='application/json')

    def register_user(self,
                      firstname="deb",
                      lastname="Nsubs",
                      email="kals@gm.com",
                      password="asddfsd"):
        """
        Method for registering a user with dummy data
        """

        return self.client.post(
            'api/v2/auth/signup',
            data=json.dumps(dict(
                firstname=firstname,
                lastname=lastname,
                email=email,
                password=password
            )
            ),
            content_type='application/json'
        )

    def login_user(self, email, password):
        """
        Method for logging a user with dummy data
        """
        self.register_user()
        return self.client.post(
            'api/v2/auth/login',
            data=json.dumps(
                dict(
                    email=email,
                    password=password
                )
            ),
            content_type='application/json'
        )

    def get_token(self, email="kals@gm.com", password="asddfsd"):
        """
        Returns a user token
        """
        response = self.login_user(email, password)
        data = json.loads(response.data)
        return data['data'][0]['token']

    def post_a_message(self,

                       subject="graduation ceremony",
                       message="invitation to attend my graduation",
                       parentMessageId=1,
                       status="sent",
                       sender_id=1,
                       reciever_id=1
                       ):
        token = self.get_token()
        """
        Method for posting a message with dummy data
        """
        return self.client.post(
            'api/v2/message',
            data=json.dumps(dict(
                            subject=subject,
                            message=message,
                            parentMessageId=parentMessageId,
                            status=status,
                            sender_id=sender_id,
                            reciever_id=reciever_id

                            )
                            ), content_type='application/json',
            headers=dict(Authorization='Bearer ' + token)
        )

    def post_a_message_with_invalid_subject_keys(self,

                                                 subject="graduation ceremony",
                                                 message="invitation to attend my graduation",
                                                 parentMessageId=1,
                                                 status="sent",
                                                 sender_id=1,
                                                 reciever_id=1
                                                 ):
        token = self.get_token()
        """
        Method for posting a message with dummy data
        """
        return self.client.post(
            'api/v2/message',
            data=json.dumps(dict(
                            subjec=subject,
                            message=message,
                            parentMessageId=parentMessageId,
                            status=status,
                            sender_id=sender_id,
                            reciever_id=reciever_id

                            )
                            ), content_type='application/json',
            headers=dict(Authorization='Bearer ' + token)
        )

    def post_a_message_with_message_keys(self,

                                         subject="graduation ceremony",
                                         messa="invitation to attend my graduation",
                                         parentMessageId=1,
                                         status="sent",
                                         sender_id=1,
                                         reciever_id=1
                                        ):
        token = self.get_token()
        """
        Method for posting a message with dummy data
        """
        return self.client.post(
            'api/v2/message',
            data=json.dumps(dict(
                            subject=subject,
                            message=message,
                            parentMessageId=parentMessageId,
                            status=status,
                            sender_id=sender_id,
                            reciever_id=reciever_id

                            )
                            ), content_type='application/json',
            headers=dict(Authorization='Bearer ' + token)
        )

    def post_a_message_with_status_keys(self,

                                        subject="graduation ceremony",
                                        message="invitation to attend my graduation",
                                        parentMessageId=1,
                                        status="sent",
                                        sender_id=1,
                                        reciever_id=1
                                        ):
        token = self.get_token()
        """
        Method for posting a message with dummy data
        """
        return self.client.post(
            'api/v2/message',
            data=json.dumps(dict(
                            subjec=subject,
                            message=message,
                            parentMessageId=parentMessageId,
                            sta=status,
                            sender_id=sender_id,
                            reciever_id=reciever_id

                            )
                            ), content_type='application/json',
            headers=dict(Authorization='Bearer ' + token)
        )

    def post_a_message_with_invalid_sender_id_key_keys(self,

                                                        subject="graduation ceremony",
                                                        message="invitation to attend my graduation",
                                                        parentMessageId=1,
                                                        status="sent",
                                                        sender_=1,
                                                        reciever_id=1
                                                        ):
        token = self.get_token()
        """
        Method for posting a message with dummy data
        """
        return self.client.post(
            'api/v2/message',
            data=json.dumps(dict(
                            subjec=subject,
                            message=message,
                            parentMessageId=parentMessageId,
                            status=status,
                            sender_id=sender_id,
                            reciever_id=reciever_id

                            )
                            ), content_type='application/json',
            headers=dict(Authorization='Bearer ' + token)
        )

    def post_a_message_with_invalid_keys(self,

                       subject="graduation ceremony",
                       message="invitation to attend my graduation",
                       parentMessageId=1,
                       status="sent",
                       sender_id=1,
                       reciever_id=1
                       ):
        token = self.get_token()
        """
        Method for posting a message with dummy data
        """
        return self.client.post(
            'api/v2/message',
            data=json.dumps(dict(
                            subject=subject,
                            message=message,

                            status=status,
                            sender_id=sender_id,
                            reciever_id=reciever_id

                            )
                            ), content_type='application/json',
            headers=dict(Authorization='Bearer ' + token)
        )
    
    def post_a_message_with_invalid_subject_keys(self,

                                                 subjec="graduation ceremony",
                                                 message="invitation to attend my graduation",
                                                 status="sent",
                                                 sender_id=1,
                                                 reciever_id=1
                                                 ):
        token = self.get_token()
        """
        Method for posting a message with dummy data
        """
        return self.client.post(
            'api/v2/message',
            data=json.dumps(dict(
                            subjec=subject,
                            message=message,
                            parentMessageId=parentMessageId,
                            status=status,
                            sender_id=sender_id,
                            reciever_id=reciever_id

                            )
                            ), content_type='application/json',
            headers=dict(Authorization='Bearer ' + token)
        )

    def post_a_message_with_invalid_token(
        self,
        subject="graduation ceremony",
        message="invitation to attend my graduation",
        parentMessageId=1,
        status="sent",
        sender_id=1,
        reciever_id=1
    ):
        """
        Method for creating a massage if token is invalid
        """
        token = "wrongtoken"
        return self.client.post(
            'api/v2/message',
            data=json.dumps(dict(
                            subject=subject,
                            message=message,
                            parentMessageId=parentMessageId,
                            status=status,
                            sender_id=sender_id,
                            reciever_id=reciever_id

                            )
                            ), content_type='application/json',
            headers=dict(Authorization='Bearer ' + token)
        )

    def post_a_message_without_token(
        self,

        subject="graduation ceremony",
        message="invitation to attend my graduation",
        parentMessageId=1,
        status="sent",
        sender_id=1,
        reciever_id=1
    ):
        """
        Method for registering a user with dummy data
        """

        return self.client.post(
            'api/v2/message',
            data=json.dumps(dict(
                            subject=subject,
                            message=message,
                            parentMessageId=parentMessageId,
                            status=status,
                            sender_id=sender_id,
                            reciever_id=reciever_id

                            )
                            ), content_type='application/json'

        )

    def get_all_recieved_mail(self):
        """test get all recieved mail"""

        token = self.get_token()
        self.post_a_message()
        return self.client.get(
            'api/v2/messages',
            content_type='application/json',
            headers=dict(Authorization='Bearer ' + token)
        )

    def get_all_recieved_mail_without_token(self):
        """get all recieved mail without a token"""

        self.post_a_message()
        return self.client.get(
            'api/v2/messages', content_type='application/json')

    def get_all_recieved_mail_with_invalid_token(self):
        """get all recievd mail with invalid token"""
        token = "extreemly invalid"
        self.post_a_message()
        return self.client.get(
            'api/v2/messages', content_type='application/json',
            headers=dict(Authorization='Bearer ' + token
                         )
        )

    def get_all_recieved_mail_with_empty_inbox(self):
        """get all recieved mail with empty inbox"""
        token = self.get_token()

        return self.client.get(
            'api/v2/messages', content_type='application/json',
            headers=dict(Authorization='Bearer ' + token
                         )
        )

    def view_sent_messages(self):
        """test view all sent messages"""
        token = self.get_token()
        self.post_a_message()
        return self.client.get(
            'api/v2/messages/sent',
            content_type='application/json',
            headers=dict(Authorization='Bearer ' + token)
        )

    def retrieve_a_message(self):
        """Method to retrieve a particular message"""
        token = self.get_token()
        self.post_a_message()
        return self.client.get(
            'api/v2/messages/1',  content_type='application/json',
            headers=dict(Authorization='Bearer ' + token)
        )

    def retrieve_a_message_given_non_existent_message_id(self):
        """Method to retrieve a particular message of a non existing user"""
        token = self.get_token()
        self.post_a_message()
        return self.client.get(
            'api/v2/messages/10',  content_type='application/json',
            headers=dict(Authorization='Bearer ' + token)
        )

    def delete_a_particular_message(self):
        """Delete a particular message given message id"""
        token = self.get_token()
        self.post_a_message()
        return self.client.delete(
            '/api/v2/messages/deleted/1',
            content_type='application/json',
            headers=dict(Authorization='Bearer ' + token)
        )

    def delete_a_particular_message_given_invalid_messageid(self):
        """Delete a particular message given an invalid message id"""
        token = self.get_token()
        self.post_a_message()
        return self.client.delete(
            '/api/v2/messages/deleted/100',  content_type='application/json',
            headers=dict(Authorization='Bearer ' + token)
        )

    def get_all_unread_messages(self):
        """Return all unread mail"""
        token = self.get_token()
        self.post_a_message()
        return self.client.get(
            '/api/v2/messages/unread', content_type='application/json',
            headers=dict(Authorization='Bearer ' + token)

        )

    def get_all_unread_messages_with_no_token(self):
        """return all unread without a token"""
        self.post_a_message()
        return self.client.get(
            '/api/v2/messages/unread', content_type='application/json'

        )

    def get_all_unread_messages_given_empty_mail_list(self):
        """Return all unread given empty mail list"""
        token = self.get_token()
        return self.client.get(
            '/api/v2/messages/unread', content_type='application/json',
            headers=dict(Authorization='Bearer ' + token)

        )

    def create_a_group(self,
                       name="abazimbi",
                       role="developers"):
        """
        Method for registering a user with dummy data
        """
        token = self.get_token()
        return self.client.post(
            'api/v2/groups',
            data=json.dumps(dict(
                name=name,
                role=role
            )
            ),
            content_type='application/json',
            headers=dict(Authorization='Bearer ' + token)
        )

    def create_a_group_with_invalid_authentication(self,
                                                   name="abazimbi",
                                                   role="developers"):
        """
        Method for registering a user with dummy data
        """
        token = "am so invalid"
        return self.client.post(
            'api/v2/groups',
            data=json.dumps(dict(
                name=name,
                role=role
            )
            ),
            content_type='application/json',
            headers=dict(Authorization='Bearer ' + token)
        )

    def create_a_group_without_authentication(self,
                                              name="abazimbi",
                                              role="developers"):
        """
        Method for creating a group without authentication
        """
        token = self.get_token()
        return self.client.post(
            'api/v2/groups',
            data=json.dumps(dict(
                name=name,
                role=role
            )
            ),
            content_type='application/json')

    def fetch_all_groups(self):
        """Method for testign fetch_all_groups"""
        token = self.get_token()
        self.create_a_group()
        return self.client.get(
            '/api/v2/groups', content_type='application/json',
            headers=dict(Authorization='Bearer ' + token)
        )

    def delete_a_group(self):
        """Delete a particular message given an invalid message id"""
        token = self.get_token()
        self.create_a_group()
        return self.client.delete(
            '/api/v2/groupss/1',  content_type='application/json',
            headers=dict(Authorization='Bearer ' + token)
        )

    def change_group_name(self, name="mothers"):
        """change group name"""
        token = self.get_token()
        self.create_a_group()
        return self.client.patch(
            '/api/v2/groups/1/name',
            data=json.dumps(dict(name=name)
                            ),
            content_type='application/json',
            headers=dict(Authorization='Bearer ' + token)
        )

    def add_members_togroup(self, userid=1, userrole="treasurer"):
        """admin can add members to a group"""
        token = self.get_token()
        self.create_a_group()
        return self.client.post(
            '/api/v2/groups/1/users',
            data=json.dumps(dict(userid=userid, userrole=userrole)
                            ), content_type='application/json',
            headers=dict(Authorization='Bearer ' + token)
        )
