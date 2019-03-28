# from tests.base_test import BaseTestCase
# import json


# class Test_messages(BaseTestCase):
#     def test_create_a_group(self):
#         """
#         Test a user is successfully created a group
#         """
#         with self.client:

#             response = self.create_a_group("quackers",
#                                            "cleanhouse"
#                                            )
#             self.assertEqual(response.status_code, 200)
#             data = json.loads(response.data)
#             self.assertEqual(data['status'], 201)
#             self.assertEqual(data['data'][0]['id'], 1)
#             self.assertEqual(data['data'][0]['name'], "quackers")
#             self.assertEqual(data['data'][0]['role'], "cleanhouse")

#     def test_create_a_group_with_out_groupname(self):
#         """
#         Test a user is successfully created a group
#         """
#         with self.client:

#             response = self.create_a_group("",
#                                            "cleanhouse"
#                                            )
#             self.assertEqual(response.status_code, 200)
#             data = json.loads(response.data)
#             self.assertEqual(data['status'], 404)
#             self.assertEqual(data['error'], 'Enter name')

#     def test_create_a_group_with_out_role(self):
#         """
#         Test a user is successfully created a group
#         """
#         with self.client:

#             response = self.create_a_group("quackers",
#                                            ""
#                                            )
#             self.assertEqual(response.status_code, 200)
#             data = json.loads(response.data)
#             self.assertEqual(data['status'], 404)
#             self.assertEqual(data['error'], 'Enter role')

#     def test_create_a_group_with_wrong_name_type(self):
#         """
#         Test create a group with invalid name
#         """
#         with self.client:

#             response = self.create_a_group(1,
#                                            "cleanhouse"
#                                            )
#             self.assertEqual(response.status_code, 200)
#             data = json.loads(response.data)
#             self.assertEqual(data['status'], 404)
#             self.assertEqual(
#                 data[
#                     'error'],
#                 'name should be made up of letters')

#     def test_create_a_group_with_wrong_role_type(self):
#         """
#         Test create a group with invalid role type
#         """
#         with self.client:

#             response = self.create_a_group("quackers",
#                                            1
#                                            )
#             self.assertEqual(response.status_code, 200)
#             data = json.loads(response.data)
#             self.assertEqual(data['status'], 404)
#             self.assertEqual(
#                 data[
#                     'error'],
#                 'role should be made up of letters')

#     def test_create_group_with_invalid_authentication(self):
#         response = self.create_a_group_with_invalid_authentication("abazimbi",
#                                                                    "developers"

#                                                                    )
#         self.assertEqual(response.status_code, 401)
#         data = json.loads(response.data)
#         self.assertEqual(data['message'], 'Token Decode Failed!')

#     def test_create_group_without_authentication(self):
#         response = self.create_a_group_without_authentication("abazimbi",
#                                                               "developers"

#                                                               )
#         self.assertEqual(response.status_code, 401)
#         data = json.loads(response.data)
#         self.assertEqual(data['message'], 'Token does not exist')
