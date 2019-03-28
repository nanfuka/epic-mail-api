from tests.base_test import BaseTestCase
import json


class Test_messages(BaseTestCase):
#     def test_deleted_mail(self):
#         """
#         Test delete a mail
#         """
#         with self.client:
#             response = self.delete_a_particular_message()
#             self.assertEqual(response.status_code, 200)
#             data = json.loads(response.data)
#             self.assertEqual(data['status'], 200)
#             self.assertEqual(
#                 data["data"][0]['message'],
#                 "email successfully deleted from the system")

    def test_delete_messages_if_messageid_is_invalid(self):
        """
        Test a user is successfully created through the api
        """
        with self.client:
            response = self.delete_a_particular_message_given_invalid_messageid()
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['status'], 200)
            self.assertEqual(
                data['message'],
                'The email has been deleted successfully')
