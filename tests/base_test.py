# from flask_testing import TestCase
from app.views.views import app
import unittest
import json


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        """
        initialise the test runner
        """
        self.client = app.test_client(self)

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

    def login_user(self, email, password):
        """
        Method for logging a user with dummy data
        """
        self.register_user()
        return self.client.post(
            'api/v1/auth/login',
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
        Method for registering a user with dummy data
        """
    #     return self.client.get('/', content_type = 'application/json', headers=dict(Authorization='Bearer ' + token))

        return self.client.post(
            'api/v1/message',
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
    # def get_all_recieved_mail(self, email="kals@gm.com", password="asddfsd"):

    def get_all_recieved_mail(self):
        token = self.get_token()
        self.post_a_message()
        return self.client.get(
            'api/v1/messages', content_type='application/json', headers=dict(Authorization='Bearer ' + token
                                                                             )
        )

    def view_sent_messages(self):
        token = self.get_token()
        self.post_a_message()
        return self.client.get(
            'api/v1/messages/sent', content_type='application/json', headers=dict(Authorization='Bearer ' + token
                                                                                 )
        )

    def retrieve_a_message(self):
        self.post_a_message()
        return self.client.get(
            'api/v1/message/1'
        )

    def delete_a_particular_message(self):
        self.post_a_message()
        return self.client.delete(
            '/api/v1/message/deleted/1'
        )
