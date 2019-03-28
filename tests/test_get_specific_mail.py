from tests.base_test import BaseTestCase

import json


class Test_messages(BaseTestCase):
    def test_get_a_particular_message(self):
        """
        Test a user can get specific mail
        """
        with self.client:
            response = self.retrieve_a_message()
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['status'], 400)  
            self.assertEqual(data['error'],
                             'that message_id is not in the system')

    def test_get_mail_with_invalid_mail_id(self):
        """
        Test a user is successfully created through the api
        """
        with self.client:
            response = self.retrieve_a_message_given_non_existent_message_id()
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['status'], 200)
