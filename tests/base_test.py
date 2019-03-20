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

    def register_user(self,
                     firstname="deb",
                      lastname="Nsubs",
                      email="kals@gm.com",
                      password="asddfsd"):
        """
        Method for registering a user with dummy data
        """

        return self.client.post(
            'api/v1/signup',
            data=json.dumps(dict(
            firstname=firstname,
            lastname=lastname,
            email=email,
            password=password
            )
            ),
            content_type='application/json'
        )

  