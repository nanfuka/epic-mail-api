# from tests.base_test import BaseTestCase
# # from app.models.user import User

# import json


# class Test_messages(BaseTestCase):
#     def test_deleted_mail(self):
#         """
#         Test a user is successfully created through the api
#         """
#         with self.client:
#             response = self.delete_a_particular_message()
#             self.assertEqual(response.status_code, 200)
#             data = json.loads(response.data)
#             self.assertEqual(data['status'], 200)
#             self.assertEqual(
#                 data["data"][0]['message'],
#                 "email successfully deleted from the system")

#     def get_all_deleted_messages_if_messageid_is_invalid(self):
#         """
#         Test a user is successfully created through the api
#         """
#         with self.client:
#             response = self.delete_a_particular_message_given_invalid_messageid()
#             self.assertEqual(response.status_code, 200)
#             data = json.loads(response.data)
#             self.assertEqual(data['status'], 200)
#             self.assertEqual(
#                 data['message'],
#                 "email successfully deleted from the system")
