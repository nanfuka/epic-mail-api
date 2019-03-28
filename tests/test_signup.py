from tests.base_test import BaseTestCase
import json


class Test_registration(BaseTestCase):

    def test_index(self):
        """test return welcome message"""
        with self.client:
            response = self.get_index_page()

    def test_signup(self):
        """
        test create a new user by supplying all the necessary cridentials
        """
        with self.client:
            response = self.register_user(
                "deb", "kalungi", "deb@gmal.com", "secret")
            data = json.loads(response.data)
            self.assertEqual(data['status'], 201)
            self.assertEqual(
                data['message'], 'thanks for registering with Epic mail')
            self.assertEqual(data['data'][0]['user']['firstname'], 'deb')
            self.assertEqual(data['data'][0]['user']['lastname'], 'kalungi')
            self.assertEqual(data['data'][0]['user']['email'], 'deb@gmal.com')

    def test_signup_without_firstname(self):
        """
        test create a new user without password
        """
        with self.client:

            response = self.register_user(
                "", "kalungi", "deb@gmal.com", "secret")
            data = json.loads(response.data)
            self.assertEqual(data['error'], 'please enter the firstname')
            self.assertEqual(data['status'], 400)

    def test_signup_with_veryshort_firstname(self):
        """
        test create a new user without password
        """
        with self.client:

            response = self.register_user(
                "xcsdfsfs", "ka", "deb@ggmal.com", "secret")
            data = json.loads(response.data)
            self.assertEqual(data['error'], 'invalid lastname. its too short')
            self.assertEqual(data['status'], 400)

    def test_signup_with_specialcahr_lastname(self):
        """
        test create a new user without password
        """
        with self.client:

            response = self.register_user(
                "xcsdfsfs", "/jhgjhlb/", "deb@ggmal.com", "secret")
            data = json.loads(response.data)
            self.assertEqual(
                data['error'],
                'lastname should only be made up of letters')
            self.assertEqual(data['status'], 400)

    def test_signup_with_firstname_as_empty_space(self):
        """
        test create a new user with an empty space as the password
        """
        with self.client:

            response = self.register_user(
                " ", "kalungi", "deb@gmal.com", "secret")
            data = json.loads(response.data)
            self.assertEqual(data['error'], 'please enter the firstname')
            self.assertEqual(data['status'], 400)

    def test_signup_with_firstname_having_non_alphabet_elements(self):
        """
        test create a new user with an empty space as the password
        """
        with self.client:

            response = self.register_user(
                "1", "kalungi", "deb@gmal.com", "secret")
            data = json.loads(response.data)
            self.assertEqual(
                data['error'], 'firstname should only be made up of letters')
            self.assertEqual(data['status'], 400)

    def test_signup_with_username_having_less_than_three_letters(self):
        """
        test create a new user with an empty space as the password
        """
        with self.client:

            response = self.register_user(
                "ds", "kalungi", "deb@gmal.com", "secret")
            data = json.loads(response.data)
            self.assertEqual(data['error'], 'invalid firstname. its too short')
            self.assertEqual(data['status'], 400)

    def test_signup_with_firstname_as_empty_space(self):
        """
        test create a new user with an empty space as the password
        """
        with self.client:

            response = self.register_user(
                " ", "kalungi", "deb@gmal.com", "secret")
            data = json.loads(response.data)
            self.assertEqual(data['error'], 'please enter the firstname')
            self.assertEqual(data['status'], 400)

    def test_signup_without_lastname(self):
        """
        test create a new user without password
        """
        with self.client:
            response = self.register_user("deb", "", "deb@gmal.com", "secret")
            data = json.loads(response.data)
            self.assertEqual(data['error'], 'please enter the lastname')
            self.assertEqual(data['status'], 400)

    def test_signup_with_lastname_as_empty_space(self):
        """
        test create a new user with an empty space as the password
        """
        with self.client:
            response = self.register_user("deb", " ", "deb@gmal.com", "secret")
            data = json.loads(response.data)
            self.assertEqual(data['error'], 'please enter the lastname')
            self.assertEqual(data['status'], 400)

    def test_signup_without_email(self):
        """
        test create a new user with an empty space as the password
        """
        with self.client:

            response = self.register_user("deb", "kalungi", "", "secret")
            data = json.loads(response.data)
            self.assertEqual(data['error'], 'please enter the email')
            self.assertEqual(data['status'], 400)

    def test_signup_with_email_as_empty_space(self):
        """
        test create a new user without password
        """
        with self.client:

            response = self.register_user("deb", "kalungi", " ", "secret")
            data = json.loads(response.data)
            self.assertEqual(data['error'], 'please enter the email')
            self.assertEqual(data['status'], 400)

    def test_signup_with_invalid_email(self):
        """
        test create a new user with an empty space as the password
        """
        with self.client:

            response = self.register_user(
                "deb", "kalungi", "debgmal.com", "secret")
            data = json.loads(response.data)
            self.assertEqual(
                data['error'],
                'Invalid email, it should be in this format; kals@gma.com')
            self.assertEqual(data['status'], 400)

    def test_signup_without_firstname_firstname_field(self):
        """
        Test signup with firstname field
        """
        with self.client:

            response = self.client.post(
                'api/v2/auth/signup',
                data=json.dumps(dict(
                                    lastname="kalungi",
                                    email="deb@gmal.com",
                                    password="secret")),
                content_type='application/json')
            data = json.loads(response.data)
            self.assertEqual(data['error'], 'firstname field must be present')
            self.assertEqual(
                data['status'],
                400)

    def test_signup_without_last_field(self):
        """
        Test signup with lastname field
        """
        with self.client:

            response = self.client.post(
                'api/v2/auth/signup',
                data=json.dumps(dict(
                                    firstname="deb",
                                    email="deb@gmal.com",
                                    password="secret")),
                content_type='application/json')
            data = json.loads(response.data)
            self.assertEqual(data['error'], 'lastname field must be present')
            self.assertEqual(
                data['status'],
                400)

    def test_signup_without_email_field(self):
        """
        Test signup with email field
        """
        with self.client:

            response = self.client.post(
                'api/v2/auth/signup',
                data=json.dumps(dict(
                    firstname="deb",
                    lastname="kalungi",
                    password="secret")),
                content_type='application/json')
            data = json.loads(response.data)
            self.assertEqual(data['error'], 'email field must be present')
            self.assertEqual(
                data['status'],
                400)

    def test_signup_without_password_field(self):
        """
        Test signup with password field
        """
        with self.client:

            response = self.client.post(
                'api/v2/auth/signup',
                data=json.dumps(dict(
                                firstname="deb",
                                lastname="kalungi",
                                email="deb@gmal.com")),
                content_type='application/json')
            data = json.loads(response.data)
            self.assertEqual(data['error'], 'password field must be present')
            self.assertEqual(
                data['status'],
                400)

    def test_signup_without_password_value(self):
        """
        Test signup with password field
        """
        with self.client:

            response = self.client.post(
                'api/v2/auth/signup',
                data=json.dumps(dict(
                                    firstname="deb",
                                    lastname="kalungi",
                                    email="deb@gdmal.com",
                                    password="")),
                content_type='application/json')
            data = json.loads(response.data)
            self.assertEqual(data['error'], 'please enter your password')
            self.assertEqual(
                data['status'],
                400)

    def test_signup_with_weak_password_value(self):
        """
        Test signup with password field
        """
        with self.client:

            response = self.client.post(
                'api/v2/auth/signup',
                data=json.dumps(dict(
                                    firstname="deb",
                                    lastname="kalungi",
                                    email="deb@gdmal.com",
                                    password="jh")),
                content_type='application/json')
            data = json.loads(response.data)
            self.assertEqual(
                data['error'],
                "weak password, please increase password strength")
            self.assertEqual(
                data['status'],
                400)
    