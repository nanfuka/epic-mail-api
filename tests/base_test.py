from app.db import Database
from app.views.views import app
import unittest
import json


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        """
        initialise the test runner
        """
        self.client = app.test_client(self)
        self.database = Database()
        self.database.create_tables()

    def tearDown(self):
        """
        Drop the database data and remove session
        """
        # self.database.session.remove()
        # self.database.drop_all()
        self.database.cursor.execute("DROP TABLE users")

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
            'api/v1/auth/signup',
            data=json.dumps(dict(
                firstname=firstname,
                lastname=lastname,
                email=email,
                password=password
            )
            ),
            content_type='application/json'
        )

    # def login_user(self, email, password):
    #     """
    #     Method for logging a user with dummy data
    #     """
    #     self.register_user()
    #     return self.client.post(
    #         'api/v1/auth/login',
    #         data=json.dumps(
    #             dict(
    #                 email=email,
    #                 password=password
    #             )
    #         ),
    #         content_type='application/json'
    #     )

    # def get_token(self, email="kals@gm.com", password="asddfsd"):
    #     """
    #     Returns a user token
    #     """
    #     response = self.login_user(email, password)
    #     data = json.loads(response.data)
    #     return data['data'][0]['token']

    # def post_a_message(self,

    #                    subject="graduation ceremony",
    #                    message="invitation to attend my graduation",
    #                    parentMessageId=1,
    #                    status="sent",
    #                    sender_id=1,
    #                    reciever_id=1
    #                    ):
    #     token = self.get_token()
    #     """
    #     Method for posting a message with dummy data
    #     """
    #     return self.client.post(
    #         'api/v1/message',
    #         data=json.dumps(dict(
    #                         subject=subject,
    #                         message=message,
    #                         parentMessageId=parentMessageId,
    #                         status=status,
    #                         sender_id=sender_id,
    #                         reciever_id=reciever_id

    #                         )
    #                         ), content_type='application/json',
    #         headers=dict(Authorization='Bearer ' + token)
    #     )

    # def post_a_message_with_invalid_token(
    #     self,
    #     subject="graduation ceremony",
    #     message="invitation to attend my graduation",
    #     parentMessageId=1,
    #     status="sent",
    #     sender_id=1,
    #     reciever_id=1
    # ):
    #     """
    #     Method for creating a massage if token is invalid
    #     """
    #     token = "wrongtoken"
    #     return self.client.post(
    #         'api/v1/message',
    #         data=json.dumps(dict(
    #                         subject=subject,
    #                         message=message,
    #                         parentMessageId=parentMessageId,
    #                         status=status,
    #                         sender_id=sender_id,
    #                         reciever_id=reciever_id

    #                         )
    #                         ), content_type='application/json',
    #         headers=dict(Authorization='Bearer ' + token)
    #     )

    # def post_a_message_without_token(
    #     self,

    #     subject="graduation ceremony",
    #     message="invitation to attend my graduation",
    #     parentMessageId=1,
    #     status="sent",
    #     sender_id=1,
    #     reciever_id=1
    # ):
    #     """
    #     Method for registering a user with dummy data
    #     """

    #     return self.client.post(
    #         'api/v1/message',
    #         data=json.dumps(dict(
    #                         subject=subject,
    #                         message=message,
    #                         parentMessageId=parentMessageId,
    #                         status=status,
    #                         sender_id=sender_id,
    #                         reciever_id=reciever_id

    #                         )
    #                         ), content_type='application/json'

    #     )

    # def get_all_recieved_mail(self):
    #     """test get all recieved mail"""

    #     token = self.get_token()
    #     self.post_a_message()
    #     return self.client.get(
    #         'api/v1/messages',
    #         content_type='application/json',
    #         headers=dict(Authorization='Bearer ' + token)
    #     )

    # def get_all_recieved_mail_without_token(self):
    #     """get all recieved mail without a token"""

    #     self.post_a_message()
    #     return self.client.get(
    #         'api/v1/messages', content_type='application/json')

    # def get_all_recieved_mail_with_invalid_token(self):
    #     """get all recievd mail with invalid token"""
    #     token = "extreemly invalid"
    #     self.post_a_message()
    #     return self.client.get(
    #         'api/v1/messages', content_type='application/json',
    #         headers=dict(Authorization='Bearer ' + token
    #                      )
    #     )

    # def get_all_recieved_mail_with_empty_inbox(self):
    #     """get all recieved mail with empty inbox"""
    #     token = self.get_token()

    #     return self.client.get(
    #         'api/v1/messages', content_type='application/json',
    #         headers=dict(Authorization='Bearer ' + token
    #                      )
    #     )

    # def view_sent_messages(self):
    #     """test view all sent messages"""
    #     token = self.get_token()
    #     self.post_a_message()
    #     return self.client.get(
    #         'api/v1/messages/sent',
    #         content_type='application/json',
    #         headers=dict(Authorization='Bearer ' + token)
    #     )

    # def retrieve_a_message(self):
    #     """Method to retrieve a particular message"""
    #     token = self.get_token()
    #     self.post_a_message()
    #     return self.client.get(
    #         'api/v1/messages/1',  content_type='application/json',
    #         headers=dict(Authorization='Bearer ' + token)
    #     )

    # def retrieve_a_message_given_non_existent_message_id(self):
    #     """Method to retrieve a particular message of a non existing user"""
    #     token = self.get_token()
    #     self.post_a_message()
    #     return self.client.get(
    #         'api/v1/messages/10',  content_type='application/json',
    #         headers=dict(Authorization='Bearer ' + token)
    #     )

    # def delete_a_particular_message(self):
    #     """Delete a particular message given message id"""
    #     token = self.get_token()
    #     self.post_a_message()
    #     return self.client.delete(
    #         '/api/v1/messages/deleted/1',
    #         content_type='application/json',
    #         headers=dict(Authorization='Bearer ' + token)
    #     )

    # def delete_a_particular_message_given_invalid_messageid(self):
    #     """Delete a particular message given an invalid message id"""
    #     token = self.get_token()
    #     self.post_a_message()
    #     return self.client.delete(
    #         '/api/v1/messages/deleted/100',  content_type='application/json',
    #         headers=dict(Authorization='Bearer ' + token)
    #     )

    # def get_all_unread_messages(self):
    #     """Return all unread mail"""
    #     token = self.get_token()
    #     self.post_a_message()
    #     return self.client.get(
    #         '/api/v1/messages/unread', content_type='application/json',
    #         headers=dict(Authorization='Bearer ' + token)

    #     )

    # def get_all_unread_messages_with_no_token(self):
    #     """return all unread without a token"""
    #     self.post_a_message()
    #     return self.client.get(
    #         '/api/v1/messages/unread', content_type='application/json'

    #     )

    # def get_all_unread_messages_given_empty_mail_list(self):
    #     """Return all unread given empty mail list"""
    #     token = self.get_token()
    #     return self.client.get(
    #         '/api/v1/messages/unread', content_type='application/json',
    #         headers=dict(Authorization='Bearer ' + token)

    #     )
