from tests.base import BaseTestCase
# from app.models.user import User

import json


class Test_registration(BaseTestCase):

    def test_index(self):
        with self.client:
            response = self.get_index_page()
    def test_signup(self):
        """
        test create a new user by supplying all the necessary cridentials
        """
        with self.client:
            response = self.register_user("deb", "kalungi", "deb@gmal.com", "secret")
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['status'], 201)           
            self.assertEqual(data['message'], 'thanks for registering with Epic mail')
            self.assertEqual(data['data'][0]['firstname'], 'deb')
            self.assertEqual(data['data'][0]['lastname'], 'kalungi')
            self.assertEqual(data['data'][0]['email'], 'deb@gmal.com')

    def test_signup_without_firstname(self):
        """
        test create a new user without password
        """
        with self.client:

            response = self.register_user("", "kalungi", "deb@gmal.com", "secret")
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['error'], 'please enter the firstname')
            self.assertEqual(data['status'], 404)

    def test_signup_with_firstname_as_empty_space(self):
        """
        test create a new user with an empty space as the password
        """
        with self.client:

            response = self.register_user(" ", "kalungi", "deb@gmal.com", "secret")
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['error'], 'please enter the firstname')
            self.assertEqual(data['status'], 404)

    def test_signup_with_firstname_having_non_alphabet_elements(self):
        """
        test create a new user with an empty space as the password
        """
        with self.client:

            response = self.register_user("1", "kalungi", "deb@gmal.com", "secret")
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['error'], 'firstname should only be made up of letters')
            self.assertEqual(data['status'], 404)

    def test_signup_with_username_having_less_than_three_letters(self):
        """
        test create a new user with an empty space as the password
        """
        with self.client:

            response = self.register_user("ds", "kalungi", "deb@gmal.com", "secret")
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['error'], 'invalid firstname. its too short')
            self.assertEqual(data['status'], 404)

    def test_signup_with_firstname_as_empty_space(self):
        """
        test create a new user with an empty space as the password
        """
        with self.client:

            response = self.register_user(" ", "kalungi", "deb@gmal.com", "secret")
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['error'], 'please enter the firstname')
            self.assertEqual(data['status'], 404)

    def test_signup_without_lastname(self):
        """
        test create a new user without password
        """
        with self.client:

            response = self.register_user("deb", "", "deb@gmal.com", "secret")
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['error'], 'please enter the lastname')
            self.assertEqual(data['status'], 404)

    def test_signup_with_lastname_as_empty_space(self):
        """
        test create a new user with an empty space as the password
        """
        with self.client:

            response = self.register_user("deb", " ", "deb@gmal.com", "secret")
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['error'], 'please enter the lastname')
            self.assertEqual(data['status'], 404)

    def test_signup_without_email(self):
        """
        test create a new user with an empty space as the password
        """
        with self.client:

            response = self.register_user("deb", "kalungi", "", "secret")
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['error'], 'please enter the email')
            self.assertEqual(data['status'], 404)

    def test_signup_with_email_as_empty_space(self):
        """
        test create a new user without password
        """
        with self.client:

            response = self.register_user("deb", "kalungi", " ", "secret")
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['error'], 'please enter the email')
            self.assertEqual(data['status'], 404)

    def test_signup_with_invalid_email(self):
        """
        test create a new user with an empty space as the password
        """
        with self.client:

            response = self.register_user("deb", "kalungi", "debgmal.com", "secret")
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['error'], 'Invalid email, it should be in this format; kals@gma.com')
            self.assertEqual(data['status'], 404)
    def test_signup_without_firstname_firstname_field(self):
        """
        Test signup with firstname field
        """
        with self.client:
       
            response = self.client.post('api/v1/signup', data=json.dumps(dict(lastname="kalungi", email="deb@gmal.com", password="secret")),content_type='application/json')
        
            self.assertEqual(response.status_code, 200)
                     
            data = json.loads(response.data)
            self.assertEqual(data['error'], 'firstname field must be present')
    
    def test_signup_without_last_field(self):
        """
        Test signup with lastname field
        """
        with self.client:
          
            response = self.client.post('api/v1/signup', data=json.dumps(dict(firstname="deb", email="deb@gmal.com", password="secret")),content_type='application/json')
        
            self.assertEqual(response.status_code, 200)
                     
            data = json.loads(response.data)
            self.assertEqual(data['error'], 'lastname field must be present')

    def test_signup_without_email_field(self):
        """
        Test signup with email field
        """
        with self.client:
       
            response = self.client.post('api/v1/signup', data=json.dumps(dict(firstname="deb", lastname="kalungi", password="secret")),content_type='application/json')
        
            self.assertEqual(response.status_code, 200)
                     
            data = json.loads(response.data)
            self.assertEqual(data['error'], 'email field must be present')

    def test_signup_without_password_field(self):
        """
        Test signup with password field
        """
        with self.client:
       
            response = self.client.post('api/v1/signup', data=json.dumps(dict(firstname="deb", lastname="kalungi", email="deb@gmal.com")),content_type='application/json')
        
            self.assertEqual(response.status_code, 200)
                     
            data = json.loads(response.data)
            self.assertEqual(data['error'], 'password field must be present')
            
        
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
            response = self.client.post('api/v1/login', data=json.dumps(dict(email="chloe@gmail.com",password="password")),content_type='application/json')
        
            self.assertEqual(response.status_code, 200)
                     
            data = json.loads(response.data)
            self.assertEqual(data['error'], 'the email and password are invalid')

    def test_login_without_email_field(self):
        """
        Test login without email key value
        """
        with self.client:
            response = self.client.post('api/v1/login', data=json.dumps(dict(password="password")),content_type='application/json')
        
            self.assertEqual(response.status_code, 200)
                     
            data = json.loads(response.data)
            self.assertEqual(data['error'], 'Enter email field')

    def test_login_without_password_field(self):
        """
        Test login without email key value
        """
        with self.client:
            response = self.client.post('api/v1/login', data=json.dumps(dict(email="chloe@gmail.com")),content_type='application/json')
        
            self.assertEqual(response.status_code, 200)
                     
            data = json.loads(response.data)
            self.assertEqual(data['error'], 'Enter password field')

    