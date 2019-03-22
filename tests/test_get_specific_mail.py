from tests.base_test import BaseTestCase
# from app.models.user import User

import json


class Test_messages(BaseTestCase):
    def test_get_all_unread(self):
        """
        Test a user is successfully created through the api
        """
        with self.client:
            response = self.retrieve_a_message()
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['status'], 200)  
            self.assertEqual(data['data']['subject'], "bookstore")  
            self.assertEqual(data['data']['message'], 'can you shift it') 
            self.assertEqual(data['data']['parentMessageId'], 1)  
            self.assertEqual(data['data']['status'], 'draft')
            self.assertEqual(data['data']['sender_id'], 1)
            self.assertEqual(data['data']['reciever_id'], 1)

    # def test_get_recieved_messages_without_token(self):
    #     """
    #     Test a user is successfully created through the api
    #     """
    #     with self.client:
    #         response = self.get_all_unread_messages_with_no_token()
    #         self.assertEqual(response.status_code, 401)
    #         data = json.loads(response.data)
    #         self.assertEqual(data['message'], 'Token does not exist')