from tests.base_test import BaseTestCase
# from app.models.user import User

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
            self.assertEqual(data['data'][0]['subject'], "graduation ceremony")  
            self.assertEqual(data['data'][0]['message'], 'invitation to attend my graduation') 
            self.assertEqual(data['data'][0]['parentMessageId'], 1)  
            self.assertEqual(data['data'][0]['status'], 'sent')
            self.assertEqual(data['data'][0]['sender_id'], 1)
            self.assertEqual(data['data'][0]['reciever_id'], 1)

    def test_get_recieved_messages_without_token(self):
        """
        Test a user is successfully created through the api
        """
        with self.client:
            response = self.get_all_unread_messages_with_no_token()
            self.assertEqual(response.status_code, 401)
            data = json.loads(response.data)
            self.assertEqual(data['message'], 'Token does not exist')



    # def test_get_recieved_messages_with_invalid_token(self):
    #     """
    #     Test a user is successfully created through the api
    #     """
    #     with self.client:
    #         response = self.get_all_recieved_mail_with_invalid_token()
    #         self.assertEqual(response.status_code, 401)
    #         data = json.loads(response.data)
    #         self.assertEqual(data['message'], 'Token Decode Failed!')

    # def test_get_recieved_messages_if_inbox_isempty(self):
    #     with self.client:
    #         response = self.get_all_recieved_mail_with_empty_inbox()
    #         self.assertEqual(response.status_code, 200)
    #         data = json.loads(response.data)
    #         self.assertEqual(data['status'], 200)
    #         # self.assertEqual(data['message'], 'there is no recieved mail to the current reciever_id yet')