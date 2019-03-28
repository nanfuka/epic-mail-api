from tests.base_test import BaseTestCase
# from app.models.user import User

import json


class Test_messages(BaseTestCase):
    def test_get_a_particular_message(self):
        """
        Test a user can get specific mail
        """
        with self.client:
            response = self.retrieve_a_message()
            self.assertEqual(response.status_code, 200)
# #             data = json.loads(response.data)
# #             self.assertEqual(data['status'], 200)  
# #             # self.assertEqual(data['data']['subject'], "bookstore")  
# # #             self.assertEqual(data['data']['message'], 'can you shift it') 
# # #             self.assertEqual(data['data']['parentMessageId'], 1)  
# # #             self.assertEqual(data['data']['status'], 'draft')
# # #             self.assertEqual(data['data']['sender_id'], 1)
# # #             self.assertEqual(data['data']['reciever_id'], 1)

# #     def test_get_mail_with_invalid_mail_id(self):
# #         """
# #         Test a user is successfully created through the api
# #         """
# #         with self.client:
# #             response = self.retrieve_a_message_given_non_existent_message_id()
# #             self.assertEqual(response.status_code, 200)
# #             data = json.loads(response.data)
# #             self.assertEqual(data['status'], 200)
# #             self.assertEqual(data['message'], 'There isnt any mail with the given mail_id')