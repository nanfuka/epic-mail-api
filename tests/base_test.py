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

