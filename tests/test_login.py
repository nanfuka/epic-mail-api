from tests.base_test import BaseTestCase
import json


class Test_registration(BaseTestCase):
    def test_login(self):
        """
        Test a registered user  is logged in successfully through the api
        """
        with self.client:
            response = self.login_user("deb@gmal.com", "secret")
            self.assertEqual(response.status_code, 200)

    def test_login_before_signup(self):
        """
        Test login with unregistered user credentials
        """
        with self.client:
            response = self.client.post(
                'api/v2/auth/login',
                data=json.dumps(
                    dict(
                        email="chloe@gmail.com",
                        password="password")),
                content_type='application/json')

            self.assertEqual(response.status_code, 200)

            data = json.loads(response.data)
            self.assertEqual(
                data[
                    'error'],
                'the email and password you have entered are invalid')

    def test_login_without_email_field(self):
        """
        Test login without email key value
        """
        with self.client:
            response = self.client.post(
                'api/v2/auth/login',
                data=json.dumps(dict(
                    password="password")),
                content_type='application/json')

            self.assertEqual(response.status_code, 200)

            data = json.loads(response.data)
            self.assertEqual(data['error'], 'Enter email field')

    def test_login_without_password_field(self):
        """
        Test login without email key value
        """
        with self.client:
            response = self.client.post('api/v2/auth/login',
                                        data=json.dumps(dict(
                                            email="chloe@gmail.com")),
                                        content_type='application/json')

            self.assertEqual(response.status_code, 200)

            data = json.loads(response.data)
            self.assertEqual(data['error'], 'Enter password field')

    def test_login_without_password_value(self):
        """
        Test login without email key value
        """
        with self.client:
            response = self.client.post(
                'api/v2/auth/login',
                data=json.dumps(dict(
                    password="",
                    email="chloe@gmail.com")),
                content_type='application/json')

            self.assertEqual(response.status_code, 200)

            data = json.loads(response.data)
            self.assertEqual(data['error'], 'Enter your password')
            self.assertEqual(data['status'], 404)

    def test_login_without_email_value(self):
        """
        Test login without email key value
        """
        with self.client:
            response = self.client.post('api/v2/auth/login',
                                        data=json.dumps(dict(
                                            password="password", email="")),
                                        content_type='application/json')

            self.assertEqual(response.status_code, 200)

            data = json.loads(response.data)
            self.assertEqual(data['error'], 'Enter your email')
            self.assertEqual(data['status'], 404)
