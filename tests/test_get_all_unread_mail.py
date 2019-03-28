from tests.base_test import BaseTestCase
import json


class Test_messages(BaseTestCase):
    def test_get_all_unread(self):
        """
        Test a user is successfully created through the api
        """
        with self.client:
            response = self.get_all_unread_messages()
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['status'], 200)
            self.assertEqual(
                data[
                    'message'],
                'you do not have any unread mail in you inbox')

    def test_get_recieved_unreadmessages_without_token(self):
        """
        Test a user is successfully created through the api
        """
        with self.client:
            response = self.get_all_unread_messages_with_no_token()
            self.assertEqual(response.status_code, 401)
            data = json.loads(response.data)
            self.assertEqual(data['message'], 'Token does not exist')

    def test_get_recieved_unreadmessages_without_token(self):
        """
        Test a user is successfully created through the api
        """
        with self.client:
            response = self.get_all_unread_messages_given_empty_mail_list()
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['status'], 200)
